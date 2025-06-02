
        class NFTTrustScoreApp {
            constructor() {
                this.form = document.getElementById('trustScoreForm');
                this.walletInput = document.getElementById('walletAddress');
                this.submitBtn = document.getElementById('submitBtn');
                this.submitText = document.getElementById('submitText');
                this.loadingSpinner = document.getElementById('loadingSpinner');
                this.errorMessage = document.getElementById('errorMessage');
                this.resultsSection = document.getElementById('resultsSection');
                this.trustScoreValue = document.getElementById('trustScoreValue');
                this.trustMeterFill = document.getElementById('trustMeterFill');
                this.reasonsList = document.getElementById('reasonsList');
                this.nftsGrid = document.getElementById('nftsGrid');

                this.initEventListeners();
            }

            initEventListeners() {
                this.form.addEventListener('submit', this.handleSubmit.bind(this));
                this.walletInput.addEventListener('input', this.clearError.bind(this));
            }

            async handleSubmit(e) {
                e.preventDefault();
                
                const walletAddress = this.walletInput.value.trim();
                if (!walletAddress) {
                    this.showError('Please enter a wallet address');
                    return;
                }

                if (!this.isValidWalletAddress(walletAddress)) {
                    this.showError('Please enter a valid wallet address');
                    return;
                }

                this.setLoading(true);
                this.clearError();

            }


            setLoading(isLoading) {
                this.submitBtn.disabled = isLoading;
                this.submitText.style.display = isLoading ? 'none' : 'inline';
                this.loadingSpinner.style.display = isLoading ? 'block' : 'none';
            }

            showError(message) {
                this.errorMessage.textContent = message;
                this.errorMessage.style.display = 'block';
                this.errorMessage.classList.add('fade-in');
            }

            clearError() {
                this.errorMessage.style.display = 'none';
                this.errorMessage.classList.remove('fade-in');
            }

            displayResults(data) {
                const { trust_score, reasons, nft_data } = data;
                
                // Display trust score
                this.displayTrustScore(trust_score);
                
                // Display reasons
                this.displayReasons(reasons);
                
                // Display NFTs
                this.displayNFTs(nft_data);
                
                // Show results section
                this.resultsSection.style.display = 'block';
                this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }

            displayTrustScore(score) {
                this.trustScoreValue.textContent = score;
                
                // Apply color coding
                const scoreClass = this.getScoreClass(score);
                this.trustScoreValue.className = `trust-score-value ${scoreClass}`;
                this.trustMeterFill.className = `trust-meter-fill meter-${scoreClass.replace('score-', '')}`;
                
                // Animate the meter fill
                setTimeout(() => {
                    this.trustMeterFill.style.width = `${score}%`;
                }, 100);
            }

            getScoreClass(score) {
                if (score >= 80) return 'score-excellent';
                if (score >= 60) return 'score-good';
                if (score >= 40) return 'score-fair';
                return 'score-poor';
            }

            displayReasons(reasons) {
                this.reasonsList.innerHTML = '';
                
                if (!reasons || reasons.length === 0) {
                    this.reasonsList.innerHTML = '<li>No specific factors identified</li>';
                    return;
                }

                reasons.forEach((reason, index) => {
                    const li = document.createElement('li');
                    li.textContent = reason;
                    li.style.animationDelay = `${index * 0.1}s`;
                    li.classList.add('fade-in');
                    this.reasonsList.appendChild(li);
                });
            }

            displayNFTs(nftData) {
                this.nftsGrid.innerHTML = '';
                
                if (!nftData || nftData.length === 0) {
                    this.nftsGrid.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: #a0a0a0;">No NFTs found</p>';
                    return;
                }

                // Limit to 10 NFTs as requested
                const nftsToShow = nftData.slice(0, 10);
                
                nftsToShow.forEach((nft, index) => {
                    const nftCard = this.createNFTCard(nft, index);
                    this.nftsGrid.appendChild(nftCard);
                });
            }

            createNFTCard(nft, index) {
                const card = document.createElement('div');
                card.className = 'nft-card fade-in';
                card.style.animationDelay = `${index * 0.05}s`;

                const img = document.createElement('img');
                img.className = 'nft-image';
                img.src = nft.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iMTAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iIzY2NiIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0Ij5ObyBJbWFnZTwvdGV4dD4KPC9zdmc+';
                img.alt = nft.name || 'NFT';
                img.onerror = function() {
                    this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iMTAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iIzY2NiIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0Ij5ObyBJbWFnZTwvdGV4dD4KPC9zdmc+';
                };

                const content = document.createElement('div');
                content.className = 'nft-card-content';

                const name = document.createElement('div');
                name.className = 'nft-name';
                name.textContent = nft.name || 'Unnamed NFT';

                content.appendChild(name);
                card.appendChild(img);
                card.appendChild(content);

                return card;
            }
        }

        // Initialize the app when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            new NFTTrustScoreApp();
        });

        // Demo data for testing (remove in production)
        window.demoAnalyze = function() {
            const app = new NFTTrustScoreApp();
            const mockData = {
                trust_score: 87,
                reasons: [
                    "Wallet has been active for over 2 years",
                    "High-value NFT transactions detected",
                    "Consistent trading patterns observed",
                    "No suspicious activity detected",
                    "Strong community engagement"
                ],
                nft_data: [
                    { name: "Bored Ape #1234", image: "https://via.placeholder.com/200x200/667eea/ffffff?text=Ape" },
                    { name: "CryptoPunk #5678", image: "https://via.placeholder.com/200x200/764ba2/ffffff?text=Punk" },
                    { name: "Azuki #9012", image: "https://via.placeholder.com/200x200/10b981/ffffff?text=Azuki" },
                    { name: "Doodle #3456", image: "https://via.placeholder.com/200x200/f59e0b/ffffff?text=Doodle" },
                    { name: "Cool Cat #7890", image: "https://via.placeholder.com/200x200/ef4444/ffffff?text=Cat" }
                ]
            };
            app.displayResults(mockData);
        };