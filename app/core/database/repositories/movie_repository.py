from operator import ge
from sqlalchemy.orm import Session, joinedload
from app.core.database.repositories.base_repository import BaseRepository
from app.core.database.models.models import Movie, Genre
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
            .options(joinedload(Movie.genre))
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

        order_criteria = []

        if year_order_asc:
            order_criteria.append(Movie.year.asc())
        else:
            order_criteria.append(Movie.year.desc())

        if price_order_asc:
            order_criteria.append(Movie.price.asc())
        else:
            order_criteria.append(Movie.price.desc())

        smt = smt.order_by(*order_criteria)

        
        smt = smt.where(Movie.price >= price_min)
        
        if price_max is not None:
            smt = smt.where(Movie.price <= price_max)
        
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
            .execute(
                smt
            )
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
            .execute(
                smt
            )
            .scalars()
            .all()
        )
    
    def get_top_by_stock(self, n: int = 5):
        smt = (
            select(Movie)
            .order_by(Movie.stock.desc())
            .limit(n)
        )
        return (
            self.session
            .execute(
                smt
            )
            .scalars()
            .all()
        )
    
    def get_all(self
                , title_order_asc: bool = True
                , year_order_asc: bool = False
                , price_order_asc: bool = True
                , offset: int = 0
                , fetch: int = 100
                ) -> list[Movie]:
        

        smt = select(Movie)

        order_criteria = []

        if year_order_asc:
            order_criteria.append(Movie.year.asc())
        else:
            order_criteria.append(Movie.year.desc())

        if title_order_asc:
            order_criteria.append(Movie.title.asc())
        else:
            order_criteria.append(Movie.title.desc())

        if price_order_asc:
            order_criteria.append(Movie.price.asc())
        else:
            order_criteria.append(Movie.price.desc())

        smt = smt.order_by(*order_criteria)

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

