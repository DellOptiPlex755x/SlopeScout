/**
 * Main application logic for the Explore page
 */
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const searchBar = document.getElementById('mountainSearch');
    const searchResults = document.getElementById('searchResults');
    const contentContainer = document.getElementById('contentContainer');
    const backButton = document.querySelector('.back-button');
    const tempRow = document.getElementById('tempRow');
    const conditionRow = document.getElementById('conditionRow');
    const windRow = document.getElementById('windRow');
    const addParkBtn = document.getElementById('addParkBtn');

    // Mountain suggestions (just Big Bear for now as requested)
    const mountainSuggestions = ['Big Bear'];

    // Animation constants
    const ANIMATION_DURATION = 1750;

    // Animation utility functions
    const easeInOutCubic = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

    // Function to show search results
    function showSearchResults(query) {
        // Clear previous results
        searchResults.innerHTML = '';

        if (!query) {
            searchResults.style.display = 'none';
            return;
        }

        // Filter mountains that match the query
        const filteredMountains = mountainSuggestions.filter(mountain =>
            mountain.toLowerCase().includes(query.toLowerCase())
        );

        if (filteredMountains.length === 0) {
            searchResults.style.display = 'none';
            return;
        }

        // Display matching mountains
        filteredMountains.forEach(mountain => {
            const resultItem = document.createElement('div');
            resultItem.className = 'search-result-item';
            resultItem.textContent = mountain;
            resultItem.addEventListener('click', () => handleMountainSelection(mountain));
            searchResults.appendChild(resultItem);
        });

        searchResults.style.display = 'block';
    }

    // Handle mountain selection and animations
    function handleMountainSelection(selectedMountain) {
        // Reset any existing content before starting a new search
        resetPage();

        // Reset search bar to initial state if expanded
        if (document.activeElement === searchBar) {
            searchBar.blur();
        }

        // Clear text and hide results
        searchBar.value = '';
        searchResults.style.display = 'none';

        // Create a clone of the search bar for animation
        const searchBarClone = createSearchBarClone();

        // Hide the original search container
        document.querySelector('.search-container').style.opacity = '0';
        // Remove any transition to prevent conflicts with later fade-in
        document.querySelector('.search-container').style.transition = 'none';

        // Start the animation
        requestAnimationFrame(timestamp => animateSearchBar(timestamp, searchBarClone, selectedMountain));
    }

    // Reset the page to initial state
    function resetPage() {
        // Hide content container
        contentContainer.style.display = 'none';

        // Remove any existing location name displays
        const existingLocationDisplay = document.querySelector('.location-name-display');
        if (existingLocationDisplay) {
            existingLocationDisplay.remove();
        }

        // Reset weather rows animation classes
        tempRow.classList.remove('fade-in');
        conditionRow.classList.remove('fade-in');
        windRow.classList.remove('fade-in');
        addParkBtn.classList.remove('fade-in');

        // Reset mountain image opacity
        const mountainImage = document.querySelector('.mountain-image');
        if (mountainImage) {
            mountainImage.style.opacity = '0';
        }
    }

    // Create search bar clone for animation
    function createSearchBarClone() {
        const searchBarRect = searchBar.getBoundingClientRect();
        const searchBarClone = document.createElement('div');

        // Style the clone to match the search bar's initial appearance
        searchBarClone.style.position = 'fixed';
        searchBarClone.style.width = searchBarRect.width + 'px';
        searchBarClone.style.height = searchBarRect.height + 'px';
        searchBarClone.style.top = searchBarRect.top + 'px';
        searchBarClone.style.left = searchBarRect.left + 'px';
        searchBarClone.style.backgroundColor = '#FFFFFF'; // 100% opaque white
        searchBarClone.style.borderRadius = '35';
        searchBarClone.style.zIndex = '100';

        // Add the clone to the document
        document.body.appendChild(searchBarClone);

        return { element: searchBarClone, rect: searchBarRect };
    }

    // Morphing animation for the search bar
    function animateSearchBar(timestamp, searchBarClone, selectedMountain, startTime = null) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / ANIMATION_DURATION, 1);

        // Use a cubic-bezier easing function for smooth animation
        const easeProgress = easeInOutCubic(progress);

        // Calculate dimensions with complete coverage of the image area (50vh)
        const width = searchBarClone.rect.width + (window.innerWidth - searchBarClone.rect.width) * easeProgress;

        // Calculate viewport-relative height to ensure full coverage
        // Adding extra padding (20% more) to ensure it covers the entire image area on all devices
        const targetHeight = Math.max(window.innerHeight * 0.5, window.innerHeight * 0.5 + 100);
        const height = searchBarClone.rect.height + (targetHeight - searchBarClone.rect.height) * Math.pow(easeProgress, 0.7);

        const top = searchBarClone.rect.top - searchBarClone.rect.top * easeProgress;
        const left = searchBarClone.rect.left - searchBarClone.rect.left * easeProgress;
        const borderRadius = 25 * (1 - easeProgress);

        // Apply the calculated styles
        searchBarClone.element.style.width = width + 'px';
        searchBarClone.element.style.height = height + 'px';
        searchBarClone.element.style.top = top + 'px';
        searchBarClone.element.style.left = left + 'px';
        searchBarClone.element.style.borderRadius = borderRadius + 'px';

        if (progress < 1) {
            requestAnimationFrame(timestamp => animateSearchBar(timestamp, searchBarClone, selectedMountain, startTime));
        } else {
            // Animation completed
            searchBarClone.element.remove();

            // Show content and begin content animations
            showContentWithAnimation(selectedMountain);
        }
    }

    // Show content with animations
    function showContentWithAnimation(selectedMountain) {
        // Show content container
        contentContainer.style.display = 'block';

        // 3. Image Fade-In with background fade-out
        const mountainImage = document.querySelector('.mountain-image');
        mountainImage.style.opacity = '0';

        // Create a background overlay element
        const backgroundOverlay = document.createElement('div');
        backgroundOverlay.style.position = 'fixed';
        backgroundOverlay.style.top = '0';
        backgroundOverlay.style.left = '0';
        backgroundOverlay.style.width = '100%';
        backgroundOverlay.style.height = '50vh';
        backgroundOverlay.style.backgroundColor = '#FFFFFF'; // 100% opaque
        backgroundOverlay.style.zIndex = '0';
        document.body.appendChild(backgroundOverlay);

        // Create text container for location name
        const textContainer = createLocationNameDisplay(selectedMountain);
        contentContainer.appendChild(textContainer);

        // Start the image fade-in animation
        requestAnimationFrame(timestamp => fadeInImage(timestamp, mountainImage, backgroundOverlay, textContainer, selectedMountain));
    }

    // Create location name display with animation
    function createLocationNameDisplay(locationName) {
        // Create the text container for the location name
        const textContainer = document.createElement('div');
        textContainer.className = 'location-name-display'; // Add class for easier selection later
        textContainer.style.position = 'absolute';
        textContainer.style.left = '40px';
        textContainer.style.bottom = 'calc(50vh - 25px)'; // 25px from bottom of image
        textContainer.style.zIndex = '50';
        textContainer.style.display = 'flex';
        textContainer.style.lineHeight = '1';
        textContainer.style.fontWeight = 'bold';
        textContainer.style.fontSize = '70px';
        textContainer.style.color = 'white';

        // Create a single container for all letters
        const textLineContainer = document.createElement('div');
        textLineContainer.style.display = 'flex'; // Use flex to keep letters on one line

        // Format the location name text
        formatLocationName(locationName, textLineContainer);

        // Add the container to the main text container
        textContainer.appendChild(textLineContainer);

        return textContainer;
    }

    // Format location name for display
    function formatLocationName(locationName, container) {
        const hasSpace = locationName.includes(' ');
        const wordParts = locationName.split(' ');

        if (hasSpace) {
            // If there's already a space, use the parts and add extra spacing
            wordParts.forEach((word, wordIndex) => {
                // Add each letter of the word
                [...word].forEach(letter => {
                    addAnimatedLetter(letter, container);
                });

                // Add wider space between words (except after the last word)
                if (wordIndex < wordParts.length - 1) {
                    const spaceSpan = document.createElement('span');
                    spaceSpan.innerHTML = '&nbsp;'; // Single non-breaking space for reduced gap
                    spaceSpan.style.display = 'inline-block';
                    spaceSpan.style.position = 'relative';
                    spaceSpan.style.opacity = '0';
                    spaceSpan.style.transform = 'translateX(-100px)';
                    container.appendChild(spaceSpan);
                }
            });
        } else if (locationName.toLowerCase() === 'bigbear') {
            // Special case for "BigBear" - split after "Big"
            const firstPart = locationName.substring(0, 3); // "Big"
            const secondPart = locationName.substring(3);  // "Bear"

            // Add first part
            [...firstPart].forEach(letter => {
                addAnimatedLetter(letter, container);
            });

            // Add space - reduced to a single space
            const spaceSpan = document.createElement('span');
            spaceSpan.innerHTML = '&nbsp;'; // Single non-breaking space
            spaceSpan.style.display = 'inline-block';
            spaceSpan.style.position = 'relative';
            spaceSpan.style.opacity = '0';
            spaceSpan.style.transform = 'translateX(-100px)';
            container.appendChild(spaceSpan);

            // Add second part
            [...secondPart].forEach(letter => {
                addAnimatedLetter(letter, container);
            });
        } else {
            // For any other text, just show as is
            [...locationName].forEach(letter => {
                addAnimatedLetter(letter, container);
            });
        }
    }

    // Add an animated letter to the container
    function addAnimatedLetter(letter, container) {
        const span = document.createElement('span');
        span.textContent = letter;
        span.style.display = 'inline-block';
        span.style.position = 'relative';
        span.style.opacity = '0';
        span.style.transform = 'translateX(-100px)';
        container.appendChild(span);
    }

    // Animate image fade-in and background fade-out
    function fadeInImage(timestamp, mountainImage, backgroundOverlay, textContainer, selectedMountain, startTime = null) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / ANIMATION_DURATION, 1);

        // Increase image opacity to 100% as background fades out
        mountainImage.style.opacity = progress;

        // Decrease background opacity to 0%
        backgroundOverlay.style.opacity = 1 - progress;

        if (progress < 1) {
            requestAnimationFrame(timestamp => fadeInImage(timestamp, mountainImage, backgroundOverlay, textContainer, selectedMountain, startTime));
        } else {
            // Remove the background overlay when animation is complete
            backgroundOverlay.remove();

            // Animate location name letters
            animateLocationLetters(textContainer.firstChild);

            // Image fade-in complete, continue with the rest
            fetchWeatherData(selectedMountain);

            // Reset animations for weather rows
            tempRow.classList.remove('fade-in');
            conditionRow.classList.remove('fade-in');
            windRow.classList.remove('fade-in');
            addParkBtn.classList.remove('fade-in');

            // Prepare search container for fade-in animation
            const searchContainer = document.querySelector('.search-container');
            searchContainer.style.opacity = '0';
            searchContainer.style.transition = 'opacity 2s ease';

            // Trigger sequential animations
            setTimeout(() => tempRow.classList.add('fade-in'), 200);

            // Start fading in the search container when first data appears
            setTimeout(() => {
                searchContainer.style.opacity = '0.3';
            }, 200);

            setTimeout(() => {
                searchContainer.style.opacity = '0.6';
                conditionRow.classList.add('fade-in');
            }, 800);

            setTimeout(() => {
                searchContainer.style.opacity = '1';
                windRow.classList.add('fade-in');
            }, 1400);

            setTimeout(() => addParkBtn.classList.add('fade-in'), 2000);

            // Ensure search bar opacity is 100% after animations complete
            setTimeout(() => {
                searchContainer.style.opacity = '1';
                // Force browser to apply the style
                void searchContainer.offsetWidth;
            }, 2500);
        }
    }

    // Animate each letter of the location name
    function animateLocationLetters(textLineContainer) {
        // Get all spans
        const allSpans = Array.from(textLineContainer.children);

        // Animate each letter with different timing based on final position
        allSpans.forEach((span, idx) => {
            // Set up the animation with different timing for each letter
            span.style.transition = `transform 1.75s cubic-bezier(0.25, 1, 0.5, 1), opacity 1.75s ease`;

            // Slightly stagger the start times for a more natural effect
            setTimeout(() => {
                span.style.opacity = '1';
                span.style.transform = 'translateX(0)';
            }, 50 * idx);
        });
    }

    // Event listeners
    searchBar.addEventListener('input', () => {
        showSearchResults(searchBar.value);
    });

    searchBar.addEventListener('focus', () => {
        if (searchBar.value) {
            showSearchResults(searchBar.value);
        }
    });

    // Hide search results when clicking outside
    document.addEventListener('click', (event) => {
        if (!searchBar.contains(event.target) && !searchResults.contains(event.target)) {
            searchResults.style.display = 'none';
        }
    });

    // Back button functionality
    backButton.addEventListener('click', () => {
        window.location.href = '../../index.html';
    });

    // Add park button functionality
    addParkBtn.addEventListener('click', () => {
        alert('Park added to your favorites!');
        // Here you would typically save this to user preferences
    });
});