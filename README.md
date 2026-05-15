# GREENPULSE • Birthday Edition 2026

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-blue.svg?longCache=true&style=plastic)](https://www.python.org/)

<p>
A premium, cinematic birthday tribute experience designed with luxury editorial aesthetics. This project features a high-fidelity scattered gallery, professional storytelling cards, a dynamic soul-word cloud, and an integrated gift delivery system. 
</p>
<br>
<small><strong>Note:</strong> Optimized for high-performance, cinematic motion across modern browsers. </small>

---

### 🌟 Key Features
- **Cinematic Storytelling:** Editorial cards highlighting professional strengths and milestones.
- **Nostalgic Gallery:** A floating 2x3 grid of personal memories with thematic "Mix" captions.
- **Interactive Gift:** Asynchronous backend integration to trigger a personalized birthday surprise.
- **Modern UI:** Built with Vanilla CSS, glassmorphism, and premium typography.

> [!IMPORTANT]
> **First Release Note (v1.0.0):** This version marks the transition from a traditional birthday template to a high-fidelity cinematic experience, finalized on May 15, 2026.

<h2>Demo<h2>

![](demo/demo.gif)

<br>

<h2> Download and Installation</h2>
<ul>
<li> Clone the repository</li>
<pre>git clone https://github.com/boudhayan-dev/Birthday</pre>
<li> Set few environment variables </li>
<pre>
""" I have used Gmail. If another service is used then set the following optional variables as well.
    set MAIL_SERVER = mail_server_host
    set MAIL_PORT = mail_server_port
"""
cd Bday-flask<br>
set MAIL_USERNAME = sender's email address<br>
set MAIL_PASSWORD = sender's password<br>
set MAIL_RECEIVER = receiver's email address
</pre>
<small><strong>Note:</strong></small> use <code> export </code> instead of <code>set</code> in case of Linux.

The above creds will be used to login in the website.
<li>Create virtual environment and activate it</li>
<pre>
virtualenv venv
</pre>
<li>Activate the virtualenv</li>
<pre>
cd venv/Scripts<br>
activate
cd ../../
</pre>
<li>Install all dependencies</li>
<pre>
pip install -r requirements.txt
</pre>
<li>Create a user for accessing the site</li>
<pre>
flask db init<br>
python util/create_user.py username password<br>
flask db migrate -m "Created admin user"<br>
flask db upgrade
</pre>
<li> Run</li>
<pre>
flask run
</pre>
</ul>



<small>© 2019 Boudhayan Dev.  All rights reserved.</small>
