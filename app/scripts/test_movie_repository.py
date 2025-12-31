from sqlalchemy import desc
from app.core.database.connection import db_connection
from app.core.database.repositories.movie_repository import MovieRepository
from app.core.database.models.movies import Movie

def main():
    with db_connection.get_session() as db:
        repo = MovieRepository(db)

        movie = Movie(
            title="Alien",
            director="Ridley Scott",
            year=1979,
            genre="Sci-Fi",
            duration=117,
            rating=9,
            description="Sci-fi horror",
            price=9.99,
        )

        repo.create(movie)
        db.commit()
        print("CREATED:", movie.id)

        fetched = repo.get_by_id(movie.id)
        print("FETCHED:", fetched.title)

        fetched.rating = 10
        repo.update(fetched)
        db.commit()
        print("UPDATED:", fetched.rating)

        repo.delete(fetched)
        db.commit()
        print("DELETED")

if __name__ == "__main__":
    main()
