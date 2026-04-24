import json
import os

from flask import Flask, render_template, request, redirect, url_for

FILENAME = "data/blog_posts.json"

app = Flask(__name__)


def load_data(file_path):
    """
    Loads a JSON file
    :param file_path: path to file
    :return: blog_posts
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    return []  # or {} depending on your use case


def write_data(file_path, data):
    """ write into a JSON file
    :param file_path: path to file
    :param data: data to write
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


@app.route('/')
def index():
    """Renders the home page"""
    blog_posts = load_data(FILENAME)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    adds a new blog_post
    :return: home page for POST, add page for GET
    """
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        blog_posts = load_data(FILENAME)
        id_post = len(blog_posts) + 1
        blog_posts.append({"id": id_post, "author": author, "title": title, "content": content})
        write_data(file_path=FILENAME, data=blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    deletes a blog_post
    :param post_id: post id to delete
    :return: redirect to home page
    """
    blog_posts = load_data(FILENAME)
    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    for i, post in enumerate(blog_posts, start=1):
        post["id"] = i

    write_data(file_path=FILENAME, data=blog_posts)

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
    blog_posts = load_data(FILENAME)
    post = fetch_post_by_id(post_id, blog_posts)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        for post in blog_posts:
            if post["id"] == post_id:
                post["author"] = author
                post["title"] = title
                post["content"] = content
                break

        # Update the post in the JSON file
        write_data(file_path=FILENAME, data=blog_posts)
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
    write_data(file_path=FILENAME, data=blog_posts)

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
