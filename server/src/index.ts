import { XMLParser } from 'fast-xml-parser';

export default {
    async fetch(request, env, ctx): Promise<Response> {
        const url = new URL(request.url);

        if (url.pathname === '/weather/realtime' && request.method === 'GET') {
            const lat = url.searchParams.get('lat');
            const lon = url.searchParams.get('lon');
            if (!lat || !lon) {
                return new Response('>:( lat long required !', { status: 400 });
            }

            try {

                const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`;
                const weatherResponse = await fetch(weatherUrl);
                
                if (!weatherResponse.ok) {
                    throw new Error('Failed to fetch forecast data');
                }

                const weatherData = await weatherResponse.json();

                const weatherCode = weatherData.current_weather.weathercode;
                const bitmap = getWeatherBitmap(weatherCode);

                const enhancedResponse = {
                    ...weatherData,
                    current_weather: {
                        ...weatherData.current_weather,
                        weather_bitmap: bitmap,
                        weathercode: weatherCode
                    }
                };

                return new Response(JSON.stringify(enhancedResponse), { 
                    headers: { 'Content-Type': 'application/json' } 
                });
            } catch (error) {
                return new Response(`weather broken :(  ${error.message}`, { status: 500 });
            }
        }

        if (url.pathname === '/weather/forecast' && request.method === 'GET') {
            const lat = url.searchParams.get('lat');
            const lon = url.searchParams.get('lon');
            if (!lat || !lon) {
                return new Response('>:( lat long required !', { status: 400 });
            }

            try {
                const forecastUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=auto&forecast_days=3`;
                const forecastResponse = await fetch(forecastUrl);
                
                if (!forecastResponse.ok) {
                    throw new Error(forecastResponse.statusText);
                }

                const forecastData = await forecastResponse.json();

                const enhancedDaily = {
                    ...forecastData.daily,
                    weather_bitmaps: forecastData.daily.weather_code.map((code: number) => getWeatherBitmap(code))
                };

                const enhancedResponse = {
                    ...forecastData,
                    daily: enhancedDaily
                };

                return new Response(JSON.stringify(enhancedResponse), { 
                    headers: { 'Content-Type': 'application/json' } 
                });
            } catch (error) {
                return new Response(`forecast broken :( ${error.message}`, { status: 500 });
            }
        }
        
        if (url.pathname === '/news' && request.method === 'GET') {
            const lang = url.searchParams.get('lang') || 'en-US';
            
            try {

                const newsUrl = `https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB/?hl=${lang}&gl=${lang.split('-')[1]}&ceid=${lang.split('-')[1]}:${lang.split('-')[0]}`;
                
                const newsResponse = await fetch(newsUrl);
                
                if (!newsResponse.ok) {
                    throw new Error('Failed to fetch news data');
                }

                const newsText = await newsResponse.text();
                const parser = new XMLParser();
                const xmlDoc = parser.parse(newsText);

                const items = xmlDoc.rss.channel.item;

                
                const formattedNews = Array.from(items.slice(0, 3)).map(item => {

                    const titleText = item.title.replace(/<[^>]*>/g, '')
                        .replace(/&nbsp;/g, ' ')
                        .replace(/\s+/g, ' ')
                        .split(' • ')
                        .map(text => text.trim())
                        .filter(text => text.length > 0)
                        .join(' - ')
                        .normalize('NFKD').replace(/[\u0300-\u036f]/g, '')
                        .replace(/&quot;/g, '"')
                        .replace(/&amp;/g, '&')
                        .slice(0, 150);
        
                    return {
                        title: titleText,
                        link: item.link,
                        pubDate: item.pubDate,
                    };
                });

                return new Response(JSON.stringify({
                    language: lang,
                    articles: formattedNews
                }), {
                    headers: { 
                        'Content-Type': 'application/json',
                        'Cache-Control': 'public, max-age=300'
                    }
                });
            } catch (error) {
                return new Response(`news broken : ${error.message}`, { 
                    status: 500,
                    headers: { 'Content-Type': 'application/json' }
                });
            }
        }

        return new Response('Hello pixel world');
    },
} satisfies ExportedHandler<Env>;

function getWeatherBitmap(weatherCode: number): number[][] {

    const bitmaps: { [key: string]: number[][] } = {
        sun: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 4, 4, 4, 4, 4, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
		cloud: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        rain: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 10, 0, 0, 10, 0, 0, 10, 0, 0, 0, 0], [0, 0, 0, 0, 10, 0, 0, 10, 0, 0, 10, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        snow: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        sun_with_cloud: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 3, 3, 3, 3, 3, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 4, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 3, 4, 4, 0, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 3, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    };

    if ([0].includes(weatherCode)) {
        return bitmaps.sun;
    } else if ([1, 2, 3, 45, 48].includes(weatherCode)) {
        return bitmaps.cloud;
    } else if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99].includes(weatherCode)) {
        return bitmaps.rain;
    } else if ([71, 73, 75, 77, 85, 86].includes(weatherCode)) {
        return bitmaps.snow;
    } else if ([0, 1, 2, 3].includes(weatherCode)) {
        return bitmaps.sun_with_cloud;
    }

    return bitmaps.cloud;
}

