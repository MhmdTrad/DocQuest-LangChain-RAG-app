css = '''
<style>
        /* Style for page title */
        .title {
            color: white;
            font-weight: bold;
        }
        
        /* Style for header */
        .header {
            color: black;
            font-weight: bold;
        }

.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}

.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  float: right;
   margin-left: 10px;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}

'''
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/6134/6134346.png" style="max-height: 75px; max-width: 75px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''



# URL of the image
image_url = "https://www.wallpapertip.com/wmimgs/15-157566_ols-bookshelf-full-of-books.jpg"

# CSS for setting background image
background_css = f"""
    <style>
        body {{
            background-image: url("{image_url}");
            background-size: cover;
        }}
    </style>
"""

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://www.wallpapertip.com/wmimgs/15-157566_ols-bookshelf-full-of-books.jpg");
  background-size: cover;
}
</style>
'''

footer="""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
        }

        .footer p {
            font-weight: bold;
            font-size: 0.9em;
        }
    </style>
    <div class="footer">
        <p>For Feedback: 
            <a href="https://www.linkedin.com/in/mohammad-al-fuqaha-a-1453861b9/" target="_blank">Mohammad Al-Fuqaha'a</a>
        </p>
    </div>
"""
