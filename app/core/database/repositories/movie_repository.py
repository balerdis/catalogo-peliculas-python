from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.models import Movie
from sqlalchemy import select, or_, func


class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: Session):
        super().__init__(Movie, session)
    
    def search(self, 
               search: str | None = None,
               offset: int = 0,
               fetch: int = 100
               ) -> list[Movie]:
        
        smt = select(Movie)

        if search:
            pattern = f"%{search}%"
            smt = smt.where(
                or_(
                    Movie.title.ilike(pattern),
                    Movie.director.ilike(pattern),
                    Movie.genre.ilike(pattern),
                )
            )
        fetch = min(fetch, 100)
        return (
            self.session
            .execute(
                smt
                .offset(offset)
                .limit(fetch)
            )
            .scalars()
            .all()
        )
    
    def get_reporte_resumen(self):
        smt = (
            select(
                func.count().label("total_units"),
                func.sum(Movie.price).label("total_price"),
                func.count(
                    func.distinct(
                        func.concat(Movie.title, '|', Movie.director)
                    )
                ).label("total_movies")
            )
            .select_from(Movie)
        )
        return (
            self.session
            .execute(
                smt
            )
            .one()
        )

