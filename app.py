<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>חיפוש</title>
    <style>
        body { 
            text-align: center; 
            font-family: Arial, sans-serif; 
            direction: rtl; 
            background-color: #fff; 
        }

        .container { 
            max-width: 650px;  
            margin: auto; 
            padding: 20px; 
        }

        .search-box {
            width: 100%;
            background: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        select, input, button {
            font-size: 16px;
            border: none;
            outline: none;
            background: none;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }

        button {
            cursor: pointer;
            padding: 10px 15px;
        }

        .top-bar {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: #ddd;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <h1>חיפוש במאגר אנשי קשר</h1>
        {% if session['user'] %}
            <a href="/logout">התנתק</a>
        {% else %}
            <a href="/login">התחבר</a>
        {% endif %}
    </div>
    
    <div class="container">
        <form action="/search" method="GET">
            <div class="search-box">
                <select name="search_type">
                    <option value="free">חיפוש חופשי</option>
                    <option value="name">שם</option>
                    <option value="title">טייטל</option>
                </select>
                <input type="text" name="query" placeholder="מה תרצה לחפש?">
                <button type="submit">חפש</button>
            </div>
        </form>
    </div>
</body>
</html>
