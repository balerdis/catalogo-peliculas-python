from sqlalchemy.orm import Session, contains_eager
from app.core.database.repositories.base_repository import BaseRepository
from app.core.database.models.movies import Movie
from app.core.database.models.genres import Genre
from sqlalchemy import select, or_, func



class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: Session):
        super().__init__(Movie, session)
    
    def search(self, 
               search: str | None = None,
               year_order_asc: bool = True,
               price_order_asc: bool = True,
               price_min: float = 0.0,
               price_max: float | None = None,
               offset: int = 0,
               fetch: int = 100
               ) -> list[Movie]:
        
        smt = (
            select(Movie)
            .join(Movie.genre)
            .options(contains_eager(Movie.genre))
        )

        if search:
            pattern = f"%{search}%"
            smt = smt.where(
                or_(
                    Movie.title.ilike(pattern),
                    Movie.director.ilike(pattern),
                    Genre.name.ilike(pattern),
                )
            )

        smt = smt.where(Movie.price >= price_min)
        
        if price_max is not None:
            smt = smt.where(Movie.price <= price_max)

        order_criteria = [
            Movie.year.asc() if year_order_asc else Movie.year.desc(),
            Movie.price.asc() if price_order_asc else Movie.price.desc(),
        ]

        smt = smt.order_by(*order_criteria)

        return (
            self.session
            .execute(
                smt
                .offset(offset)
                .limit(min(fetch, 100))
            )
            .scalars()
            .unique()
            .all()
        )
    
    def get_reporte_resumen(
            self
            , genre: str | None = None
            , director: str | None = None
            , year_from: int | None = None
            , year_to: int | None = None
        ):
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
            .join(Movie.genre)
        )

        if genre:
            smt = smt.where(Genre.name.ilike(f"%{genre}%"))
        
        if director:
            smt = smt.where(Movie.director.ilike(f"%{director}%"))

        if year_from is not None:
            smt = smt.where(Movie.year >= year_from)

        if year_to is not None:
            smt = smt.where(Movie.year <= year_to)

        return (
            self.session
            .execute(smt)
            .one()
        )
    
    def get_top_by_price(self, n: int = 5):
        smt = (
            select(Movie)
            .order_by(Movie.price.desc())
            .limit(n)
        )
        return (
            self.session
            .execute(smt)
            .scalars()
            .all()
        )
    
    def get_all_ordered(self
                , title_order_asc: bool = True
                , year_order_asc: bool = False
                , price_order_asc: bool = True
                , offset: int = 0
                , fetch: int = 100
                ) -> list[Movie]:
        

        smt = select(Movie)

        order_criteria = [
            Movie.year.asc() if year_order_asc else Movie.year.desc(),
            Movie.title.asc() if title_order_asc else Movie.title.desc(),
            Movie.price.asc() if price_order_asc else Movie.price.desc(),
        ]

        smt = smt.order_by(*order_criteria)

        return (
            self.session
            .execute(smt
                .offset(offset)
                .limit(fetch)
            )
            .scalars()
            .all()
        )

