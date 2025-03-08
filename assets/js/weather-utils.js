/**
 * Weather utility functions for SlopeScout
 */

// Function to convert weather code to readable condition
function getWeatherCondition(code) {
    // WMO Weather interpretation codes (https://open-meteo.com/en/docs)
    const weatherCodes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        56: 'Light freezing drizzle',
        57: 'Dense freezing drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        66: 'Light freezing rain',
        67: 'Heavy freezing rain',
        71: 'Slight snow fall',
        73: 'Moderate snow fall',
        75: 'Heavy snow fall',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail'
    };

    return weatherCodes[code] || 'Unknown';
}

// Function to get wind direction from degrees
function getWindDirection(degrees) {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const index = Math.round(degrees / 45) % 8;
    return directions[index];
}

// Function to update weather icon based on conditions
function updateWeatherIcon(weatherCode) {
    const weatherIcon = document.querySelector('.weather-row:nth-child(2) .weather-icon i');

    // Clear previous classes except for 'fas'
    weatherIcon.className = '';
    weatherIcon.classList.add('fas');

    // Set appropriate icon based on weather code
    if (weatherCode <= 1) {
        weatherIcon.classList.add('fa-sun');
    } else if (weatherCode <= 3) {
        weatherIcon.classList.add('fa-cloud-sun');
    } else if (weatherCode <= 48) {
        weatherIcon.classList.add('fa-smog');
    } else if (weatherCode <= 57) {
        weatherIcon.classList.add('fa-cloud-rain');
    } else if (weatherCode <= 67) {
        weatherIcon.classList.add('fa-cloud-showers-heavy');
    } else if (weatherCode <= 77) {
        weatherIcon.classList.add('fa-snowflake');
    } else if (weatherCode <= 82) {
        weatherIcon.classList.add('fa-cloud-rain');
    } else if (weatherCode <= 86) {
        weatherIcon.classList.add('fa-snowflake');
    } else {
        weatherIcon.classList.add('fa-bolt');
    }
}

// Function to fetch weather data from API
async function fetchWeatherData(location) {
    try {
        // For Big Bear, using approximate coordinates
        const latitude = 34.2439;
        const longitude = -116.9114;

        const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,weather_code,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Weather data not available');
        }

        const data = await response.json();

        // Get UI elements
        const tempValue = document.getElementById('tempValue');
        const windValue = document.getElementById('windValue');
        const windDirection = document.getElementById('windDirection');
        const conditionValue = document.getElementById('conditionValue');

        // Update the UI with weather data
        const temperature = Math.round(data.current.temperature_2m);
        const windSpeed = Math.round(data.current.wind_speed_10m);
        const windDir = getWindDirection(data.current.wind_direction_10m);
        const weatherCode = data.current.weather_code;
        const conditions = getWeatherCondition(weatherCode);

        tempValue.textContent = temperature;
        windValue.textContent = windSpeed;
        windDirection.textContent = windDir;
        conditionValue.textContent = conditions;

        // Update weather icon based on conditions
        updateWeatherIcon(weatherCode);

    } catch (error) {
        console.error('Error fetching weather data:', error);

        // Get UI elements
        const tempValue = document.getElementById('tempValue');
        const conditionValue = document.getElementById('conditionValue');
        const windValue = document.getElementById('windValue');
        const windDirection = document.getElementById('windDirection');

        // Set default values on error
        tempValue.textContent = '--';
        conditionValue.textContent = 'Data unavailable';
        windValue.textContent = '--';
        windDirection.textContent = '';
    }
}