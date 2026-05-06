from flask import Flask, render_template, request, redirect, url_for
from database import load_data, write_data

app = Flask(__name__)


def format_post_content(content):
    """
    Converts line breaks into HTML <br/> tags
    :param content: raw post content
    :return: formatted HTML content
    """
    return content.replace("\r\n", "<br/>").replace("\n", "<br/>")


@app.route('/')
def index():
    """Renders the home page"""
    blog_posts = load_data()

    for post in blog_posts:
        post["content"] = format_post_content(post["content"])

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    adds a new blog_post
    :return: home page for POST, add page for GET
    """
    if request.method == 'POST':
        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        blog_posts = load_data()

        if blog_posts:
            id_post = max(post["id"] for post in blog_posts) + 1
        else:
            id_post = 1

        blog_posts.append({"id": id_post, "author": author, "title": title, "content": content})
        write_data(data=blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    deletes a blog_post
    :param post_id: post id to delete
    :return: redirect to home page
    """
    blog_posts = load_data()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    write_data(data=blog_posts)

    return redirect(url_for('index'))


def fetch_post_by_id(post_id, posts):
    """
    fetches a blog_post
    :param post_id: post id to fetch
    :param posts: posts to fetch
    :return: post
    """
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    updates a blog_post
    :param post_id: post id to update
    :return: redirect to home page for POST, update page for GET
    """
    # Fetch the blog posts from the JSON file
    blog_posts = load_data()
    post = fetch_post_by_id(post_id, blog_posts)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':

        author = request.form.get('author').strip()
        title = request.form.get('title').strip()
        content = request.form.get('content').strip()
        for post in blog_posts:
            if post["id"] == post_id:
                post["author"] = author
                post["title"] = title
                post["content"] = content
                break

        # Update the post in the JSON file
        write_data(data=blog_posts)
        # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


def main():
    """
    main function
    """
    blog_posts = [
        {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
        {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
        # More blog posts can go here...
    ]
    write_data(data=blog_posts)

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
