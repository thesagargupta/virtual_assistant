<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download Anu Assistant</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Global Styling */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f5;
            margin: 0;
            padding: 0;
            color: #333;
            line-height: 1.6;
            text-align: center;
        }

        h1, h2, p {
            margin: 0;
            padding: 10px 0;
        }

        /* Container for all sections */
        .container {
            width: 100%;
            max-width: 1200px; /* Ensures content doesn't stretch too wide */
            margin: 0 auto; /* Centers the content horizontally */
            padding: 20px;
            box-sizing: border-box;
        }

        /* First Section */
        .first {
            margin-top: 20px;
            padding: 20px;
            background-color: #34495e;
            color: white;
            font-size: 1.3rem;
            border-radius: 10px;
            max-width: 600px;
            margin: 20px auto; /* Centers this section */
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Added shadow */
        }

        .first:hover {
            background-color: #2c3e50;
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.4); /* Shadow on hover */
        }

        /* Download Button */
        .second {
            text-align: center;
            margin: 20px auto;
        }

        .second .btn {
            background-color: #3498db;
            color: white;
            padding: 15px 25px;
            border: none;
            border-radius: 5px;
            font-size: 1.2rem;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Added shadow */
        }

        .second .btn:hover {
            background-color: #2980b9;
            transform: scale(1.05);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3); /* Shadow on hover */
        }

        /* Box Styling for "Please read about Anu Assistant" */
        .read-box {
            background-color: #e74c3c;
            color: white;
            padding: 20px;
            border-radius: 10px;
            max-width: 800px;
            margin: 20px auto; /* Centers this section */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Added shadow */
            border: 2px solid #c0392b;
            font-size: 1.2rem;
            font-weight: bold;
            position: relative;
            transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
        }

        .read-box::after {
            content: "👇👇";
            position: absolute;
            bottom: -10px;
            right: 50%;
            transform: translateX(50%);
            font-size: 2rem;
        }

        .read-box:hover {
            background-color: #c0392b;
            transform: scale(1.03);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.4); /* Shadow on hover */
        }

        /* Virtual Assistant Description */
        .description {
            margin: 20px auto;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 10px;
            max-width: 800px;
            font-size: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-align: center;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Added shadow */
        }

        .description:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.25); /* Shadow on hover */
        }

        /* Task and Requirements Sections */
        .tasks, .requirements {
            margin: 20px auto;
            padding: 20px;
            background-color: #ecf0f1; /* Light grey background for clarity */
            border-radius: 10px;
            max-width: 800px; /* Limit width for better readability */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); /* Shadow for depth */
            text-align: left; /* Align text to the left for readability */
            transition: box-shadow 0.3s ease;
        }

        .tasks h2, .requirements h1 {
            color: #e74c3c; /* Heading color */
            margin: 0 0 10px; /* Space below heading */
        }

        .tasks ul {
            padding-left: 20px; /* Space for list items */
            list-style-type: disc; /* Bullet points for list */
        }

        .requirements pre {
            background-color: #f0f0f0; /* Light background for code block */
            padding: 10px;
            border-radius: 5px;
            white-space: pre-wrap; /* Ensure wrapping for long lines */
            word-wrap: break-word; /* Break long words */
        }

        /* Fun Fact Section */
        .fun-fact {
            background-color: #f1c40f;
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 20px auto;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); /* Added shadow */
        }

        .fun-fact:hover {
            background-color: #f39c12;
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3); /* Shadow on hover */
        }

        .fun-fact h2, .fun-fact h1 {
            margin: 10px;
            color: #333;
        }

        /* Responsive Design */
        @media screen and (max-width: 768px) {
            .first, .read-box, .requirements, .description, .tasks, .fun-fact {
                width: 90%; /* Ensure content is responsive */
                max-width: none; /* Removes max-width constraint on smaller screens */
                padding: 10px; /* Adjust padding */
            }

            .tasks ul {
                padding-left: 15px; /* Smaller padding for lists */
            }

            .second .btn {
                padding: 10px 20px;
                font-size: 1rem;
            }

            h1, h2, p {
                font-size: 1.1rem; /* Smaller text for headings */
            }
        }

        @media screen and (max-width: 480px) {
            .first, .read-box, .requirements, .description, .tasks, .fun-fact {
                width: 95%; /* Ensure all content remains centered on smaller screens */
                padding: 5px; /* Smaller padding for very small screens */
            }

            h1, h2, p {
                font-size: 1rem; /* Further reduce text size for small screens */
            }

            .read-box::after {
                font-size: 1.5rem; /* Reduce arrow size for smaller screens */
            }

            .second .btn {
                padding: 8px 15px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="first">
            <p>To Download Annu Assistant to your PC</p>
        </div>

        <div class="second">
            <a href="main.exe" download="main.exe">
                <button type="button" class="btn">Download</button>
            </a>
        </div>

        <br>

        <p>Please read about the Anu Assistant Below 👇👇</p>

        <div class="read-box">
            <h2><u>This is my Virtual Assistant Project which I have made using Python.</u></h2>
            <br>
            <h2>Here you can perform many tasks such as playing music on Spotify, opening websites, asking for weather information, and listening to headlines.</h2>
        </div>

        <div class="description">
            <h2>Run the program and activate the assistant just by saying:</h2>
            <h1>"hello Annu"</h1>
        </div>

        <div class="tasks">
            <h2>Performing Tasks:</h2>
            <ul>
                <li>To play a song on Spotify: say "play song {song_name}"</li>
                <li>To listen to the news: say "what are the headlines today"</li>
                <li>To know the weather forecast: say "what is the weather in {your_city_name}"</li>
                <li>To open YouTube, Instagram, etc.: say "open {site name}"</li>
            </ul>
        </div>

        <div class="requirements">
            <h1>Requirements to Run This Program:</h1>
            <pre>
1) pip install PyAudio
2) pip install Pyttsx3
3) pip install requests
4) pip install spotipy
5) pip install speechrecognition
            </pre>
        </div>

        <div class="fun-fact">
            <h1>Here’s a fun fact:</h1>
            <h2>You can ask her about me 😅😅: just by saying</h2>
            <h1>"who is Sagar Gupta"</h1>
        </div>
    </div>
</body>
</html>
