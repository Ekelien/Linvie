from linvie.domain.model import Movie, Comment, User, Genre, People

movie = [Movie(n, "M" + str(n), 2000) for n in range(20)]
genre = [Genre(n, "G" + str(n)) for n in range(20)]
people = [People(n, "P" + str(n)) for n in range(20)]
user = [User(n, "U" + str(n), '0000') for n in range(2)]


def test_movie_people_model():
    people[0].participate(movie[0])
    people[1].participate(movie[0])
    people[0].direct(movie[0])
    assert people[0].is_director() == True
    assert people[0].is_actor() == True
    assert people[0].directed == [movie[0]]
    assert people[0].participated == [movie[0]]
    assert people[1].is_director() == False
    assert people[1].is_actor() == True
    assert people[1].directed == []
    assert people[1].participated == [movie[0]]


def test_user_and_favorite_model():
    user[0].like(movie[0])
    user[0].like(movie[1])
    assert user[0].favorite == movie[:2]
    user[0].dislike(movie[1])
    assert user[0].favorite == [movie[0]]


def test_comment_movie_user_model():
    c0 = Comment(0, 0, 0, 'oh')
    c1 = Comment(1, 0, 0, 'ha')
    user[0].add_comment(c0)
    user[0].add_comment(c1)
    movie[0].add_comment(c0)
    movie[0].add_comment(c1)
    assert [c.ID for c in user[0].comments] == [0, 1]
    assert [c.user_id for c in movie[0].comments] == [0, 0]
