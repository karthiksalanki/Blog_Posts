# Blog_Posts

*   Project Overview:

    *   The Blog API is a backend solution built using Django and Django REST Framework (DRF) to manage blog posts, user authentication, comments, and tags. The API ensures secure access with JWT authentication, allowing users to register, log in, and manage their own blog content. Authenticated users can create, update, and delete posts, while others can view posts.

    *   It supports user interactions through comments and tags, offering advanced features like searching, filtering posts by tags, and pagination to improve content discovery. The API is designed with performance and scalability in mind, ensuring a smooth experience for all users.

*   Features:

    * User Authentication:
        *   JWT Authentication: Secure login and access to authenticated features.
        *   User Registration & Login: APIs to register and log in users, issuing JWT tokens upon success.

    *   Blog Post Management:
        *   CRUD Operations: Authenticated users can create, update, or delete their own blog posts.
        *   Post Attributes: Includes title, content, author, creation date, and tags.
        *   Post Ownership: Only the creator can modify or delete their posts.

    *   Comments & Tags:
        *   Comments: Authenticated users can comment on any post.
        *   Most Commented Posts: API to fetch the most commented posts.
        *   Tag System: Filter posts by tags and allow users to add custom tags.

    *   Advanced Features:
        *   Pagination: Efficiently handle large lists of blog posts.
        *   Search: Search posts based on keywords in titles or content.
        *   Tag-based Filtering: Filter posts by tags without authentication.

*   Prerequisites:

    *   Python 3.x
    *   Django 3.x or higher
    *   Required packages listed in requirements.txt

*   Installation:

    *   Clone the repository:
        *    git clone https://github.com/karthiksalanki/Blog_Posts

    *   Navigate to the project directory:
        *    cd project-repository

    *   Set up a virtual environment:
        *    python -m venv venv
        *    venv\Scripts\activate   # on Linux venv/bin/activate

    *   Install dependencies:
        *    pip install -r requirements.txt

    *   Set up the database(Using default sqlite3 Database or want to use mysql configure in settings.py file):
        *    python manage.py migrate

    *   Run the development server:
        *    python manage.py runserver
