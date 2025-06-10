from django.shortcuts import render
from .models import Wallet, Score
from .forms import WalletForm
import requests
from django.conf import settings
import json
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from account.models import Profile
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator


@login_required
def home(request):
    form = WalletForm()
    nft_data = None
    url = None
    trust_score = 0
    reasons = []

    blue_chip_contracts = [
        "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",  # Bored Ape Yacht Club
        "0xbd3531da5cf5857e7cfaa92426877b022e612cf8",  # Pudgy Penguins
        "0x3b3ee1931dc30c1957379fac9aba94d1c48a5405",  # Foundation
    ]

    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Wallet.objects.create(name=name)

            url = f'https://deep-index.moralis.io/api/v2.2/nft/{name}'
            headers = {
                'accept': 'application/json',
                'X-API-Key': settings.MORALIS_API_KEY
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                nfts = response.json().get('result', [])[0:10]
                
                # Parse metadata
                for nft in nfts:
                    try:
                        nft['parsed_metadata'] = json.loads(nft.get('metadata', '{}'))
                    except:
                        nft['parsed_metadata'] = {}

                nft_data = nfts

                # Rule 1: Owns at least 1 NFT
                if len(nfts) > 0:
                    trust_score += 10
                    reasons.append("Owns at least 1 NFT (+10)")
                else:
                    reasons.append("Owns no NFTs (0)")

                # Rule 2: Owns NFT from trusted project
                trusted_contracts = ["0x524cab2ec69124574082676e6f654a18df49a048"]
                owns_trusted = any(nft.get('token_address', '').lower() in trusted_contracts for nft in nfts)

                if owns_trusted:
                    trust_score += 20
                    reasons.append("Owns NFT from trusted project (+20)")
                else:
                    reasons.append("No trusted NFTs found (0)")

                # Rule 3: transaction:
                txn_url = f"https://deep-index.moralis.io/api/v2.2/{name}/verbose-transactions"
                txn_headers = {
                    'accept' : 'application/json',
                    'X-API-Key' : settings.MORALIS_API_KEY
                }
                txn_response = requests.get(url, headers=headers)
                
                if txn_response.status_code == 200:
                    txn_data = txn_response.json()
                    if txn_data.get('total', 0) > 0:
                        trust_score += 15
                        response.append("Wallet has made transaction (+15)")
                    else:
                        reasons.append("No transactions found (+0)")
                else:
                    reasons.append(f"Failed to fetch transaction data (status {txn_response.status_code})")

                # Rule 4

                old_nft_found = False
                six_months_ago = datetime.now() - timedelta(days=180)

                for nft in nft_data:
                    minted_date_str = nft.get('last_metadata_sync') or nft.get('synced_at') or None


                    if minted_date_str:
                        try:
                            minted_date = datetime.strptime(minted_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                            if minted_date < six_months_ago:
                                old_nft_found = True
                                break
                        except Exception as e:
                            continue
                if old_nft_found:
                    trust_score += 10
                    reasons.append("Owns NFTs older than 6 months (+10)")
                else:
                    reasons.append("No old NFTs found (+0)")

                active_nfts = 0
                now = datetime.now(timezone.utc)
                days_30_ago = now - timedelta(days=30)

                for nft in nft_data:
                    last_sync = nft.get('last_metadata_sync') or nft.get('last_token_uri_sync')
                    if last_sync:
                        try:
                            sync_date = datetime.fromisoformat(last_sync.replace('Z', '+00:00'))  # Convert ISO to datetime
                            if sync_date > days_30_ago:
                                active_nfts += 1
                        except ValueError:
                            continue


                if active_nfts > 0:
                    trust_score += 15
                    reasons.append(f"Wallet has {active_nfts} recently active NFTs (+15)")
                else:
                    reasons.append("No recent NFT activity in the last 30 days (+0)")

                owns_blue_chip = False

                for nft in nft_data:
                    if nft.get('token_address', '').lower() in blue_chip_contracts:
                        owns_blue_chip = True
                        break
                if owns_blue_chip:
                    trust_score += 25
                    reasons.append("Owns NFT from a blue-chip project (+25)")
                else:
                    reasons.append("No blue-chip NFTs found (+0)")

                collection_address = set()

                for nft in nft_data:
                    contract_address = nft.get('token_address', '').lower()
                    if contract_address:
                        collection_address.add(contract_address)
                
                collection_count = len(collection_address)

                if collection_count >= 3:
                    trust_score += 20
                    reasons.append(f"Owns NFTs from {collection_count} collections (+15)")
                elif 1 <= collection_count < 3:
                    trust_score += 5
                    reasons.append(f"Owns NFTs from {collection_count} collections (+5)")
                else:
                    reasons.append("No collection diversity found (+0)")
            else:
                nft_data = [{'parsed_metadata': {'name': f'API failed with status {response.status_code}'}}]

    context = {
        'nft_data': nft_data,
        'url': url,
        'form': form,
        'trust_score': trust_score,
        'reasons': reasons,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }

    return render(request, 'pages/homepage.html', context)




stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        domain = 'https://trustscore.up.railway.app/'  # use your real domain in production

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price': 'price_1RYEKYRxebcXidgt16XSFQ9J',  # use your real price ID
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/'
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')  # ✅ Fix: use .get() not ()

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle subscription events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_email']
        subscription_id = session['subscription']

        try:
            profile = Profile.objects.get(user__email=customer_email)
            profile.stripe_subscription_id = subscription_id
            profile.save()
        except Profile.DoesNotExist:
            pass  # Log or handle this situation appropriately

    return HttpResponse(status=200)


def is_subscribed(user):
    profile = user.profile
    if profile.stripe_subscription_id:
        subscription = stripe.Subscription.retrieve(profile.stripe_subscription_id)
        return subscription.status == "active"
    return False


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
