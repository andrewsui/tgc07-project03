# PC Hardware Reviews

## Data-Centric Development Milestone Project
A demo of this project can be viewed [here](https://tgc07-project03.herokuapp.com/).
The sample user log in details below can be used to demo the project:
| Email | Password | Access Rights |
|-------|----------|---------------|
| admin@email.com | password123 | administrator |
| limited@email.com | password123 | limited |

This website has been designed for PC hardware enthusiasts to post their reviews on PC components. The general public are able read the reviews for free, without any requirement to login. However, to post a review, comment, or vote, registation for a user account and login are required.

The site owner is assumed to be part of the Amazon affiliate programme, enabling the website to earn affiliate referral income from any click-throughs to product purchases. 

### Disclaimer
Most, if not all, of the external links in this project direct towards actual Amazon products, however **the affiliate referral modifiers are not genuine**.

## UX

### Strategy - User Stories
Members of the public would use the website to:
- Browse reviews of PC components to make more informed decisions when buying PC products.
- Read comments made on reviews to understand other people's views and opinions.
- Post reviews to be help the PC enthusiast community.
- Post comments to share personal experiences and opinions on PC products.
- Help the PC entusiast community members with any troubleshooting problems they may have encountered.
- Easily make purchases of products via the linked product pages.
- Vote up or down if they like or dislike a review.

Owners of the website would like to:
- Earn referral income on purchases that arise from click-throughs of the site's affiliate links.
- Be able to moderate the site content via admin accounts that can edit and delete reviews and comments, to maintain a friendly and welcoming environment for all users.
- Also be users of the site, by posting and reading reviews/comments related to PC components.

### Scope
Content requirements:
- images of PC components being reviewed
- text for review content
- URLs to Amazon product pages
- icons for vote feature

Functional specification:
- vote buttons need to be able to function without requiring page to reload
- pages to separate reviews into manageable sizes so that each web page does not get too long

### Structure
The website structure will be presented using the hierarchical model. Main sections will be:
- review threads
- categories
- users

### Skeleton

### Surface

## Features

### Current Features
#### PC Component Reviews
- Ability to read all reviews, without needing to sign up for user account.
- Create, update, delete reviews that were written by yourself.
- Sort reviews by chronological order, reverse chronological order, price (low to high), price (high to low).
- Search reviews by category, sub-category and search box to query review title, review description or comments.
- Vote up or down on reviews if user has an account and is logged in, without need to reload page.
- Clicking a vote button will check if user has previously voted. If user had previously voted on same button currently clicked, then this latest action will remove the vote. If user had previously voted on the opposite vote button, then the opposite vote previously cast will be removed and the new vote cast.
- Update and delete any reviews if user has admin rights.
- Create and update review thread forms include validation steps that must be passed before being able to proceed. If there are errors, all input fields will be pre-populated with previously entered data on page reload.

#### Review Comments
- Ability to read all comments, without needing to sign up for user account.
- Create, update, delete comments that were written by yourself.

#### User accounts
- Sign up for user account, log in, log out.
- Update and delete user account details for user's own account.
- Update and delete any user account details if user has admin rights.
- Add or remove admin rights to users if current logged in user has admin rights.
- User log in and sign up forms include validation steps that must be passed before being able to proceed. If there are errors all fields except for password will be pre-populated on page reload.
- Create, update, delete categories and sub-categories if user has admin rights.

### Features Left to Implement:
- Ability to apply simple formatting of the review and comments text by using a library such as [Summernote](https://summernote.org/).
- Quote other comments previously posted.
- Sort by most up-voted or down-voted reviews.
- Stop word filtering to automatically remove pre-determined list of bad words from reviews and comments before they get posted.
- Check if username and email are unique before allowing user to create or update to them.
- Check if categories and sub-categories are unique before allowing user to create or update to them.

## Technologies Used
- Python
- HTML
- CSS
- JavaScript
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for cloud hosted database
- [Flask 1.1.2](https://flask.palletsprojects.com/en/1.1.x/) to create the web app
- [Flask-Login 0.5.0](https://flask-login.readthedocs.io/en/latest/) for user authentication
- [passlib 1.7.2](https://passlib.readthedocs.io/en/stable/) for password hashing
- [Jinja 2.11.2](https://jinja.palletsprojects.com/en/2.11.x/) for templating
- [pymongo 3.11.0](https://pymongo.readthedocs.io/) to communicate with MongoDB database using Python
- [dotenv](https://pypi.org/project/python-dotenv/) to use environment variables
- [JQuery](https://jquery.com/) for DOM manipulation
- [Axios](https://github.com/axios/axios) for AJAX calls
- [toastr](https://codeseven.github.io/toastr/) for flash messaging
- [Bootstrap 4.5](https://getbootstrap.com/docs/4.5/getting-started/introduction/) for web page styling
- [Font Awesome 4.7.0](https://fontawesome.com/v4.7.0/) for icons
- [Heroku](https://www.heroku.com/) to host the web app
- [gunicorn 20.0.4](https://gunicorn.org/) as the Python WSGI HTTP Server for deployment
- [GitHub](https://github.com/) for source control
