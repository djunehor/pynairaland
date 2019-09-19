pynairaland
===================

Note: This package was tested on Windows and Linux. Issues and pull requests welcome.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Python module to fetch and parse data from Nairaland.

Installation
------------

You will need `Python 3.x <https://www.python.org/download/>`__ and
`pip <http://pip.readthedocs.org/en/latest/installing.html>`__.

Install using pip:

::

    pip install nairaland

Usage
-----

User statistics
~~~~~~~~~~~~~~~

.. code:: python

    from nairaland import User

    user = User('Christopher-J-Su')

    # Get user activity
    activity = user.activity

    # Do stuff with the parsed activity data
    print activity

    # Get user statistics
    stats = user.stats

    # Take a gander
    print stats

Questions
~~~~~~~~~

.. code:: python

    from quora import Quora

    # Get question statistics
    question = Quora.get_question_stats('what-is-python')

    # question is:
    # {
    #     'want_answers': 3,
    #     'question_text': u'What is python?', 
    #     'topics': [u'Science, Engineering, and Technology', u'Technology', u'Electronics', u'Computers'], 
    #     'question_details': None, 'answer_count': 1, 
    #     'answer_wiki': '<div class="hidden" id="answer_wiki"><div id="ld_mqcfmt_15628"><div id="__w2_po3p1uM_wiki"></div></div></div>',
    # }

Answer statistics
~~~~~~~~~~~~~~~~~

.. code:: python

    from quora import Quora

    # The function can be called in any of the following ways.
    answer = Quora.get_one_answer('http://qr.ae/6hARL')
    answer = Quora.get_one_answer('6hARL')
    answer = Quora.get_one_answer(question, author) # question and answer are variables

    # answer is:
    # {
    #     'want_answers': 8, 
    #     'views': 197, 
    #     'author': u'Mayur-P-R-Rohith', 
    #     'question_link': u'https://www.quora.com/Does-Quora-similar-question-search-when-posing-a-new-question-work-better-than-the-search-box-ove', 
    #     'comment_count': 1, 
    #     'answer': '...', 
    #     'upvote_count': 5
    # }

    # Get the latest answers from a question
    latest_answers = Quora.get_latest_answers('what-is-python')

Features
--------

Currently implemented
~~~~~~~~~~~~~~~~~~~~~

-  User statistics
-  User activity
-  Question statistics
-  Answer statistics

To do
~~~~~

-  Detailed user information (followers, following, etc.; not just
   statistics)

