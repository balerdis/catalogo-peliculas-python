from app.core.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork

def main():
    with SqlAlchemyUnitOfWork() as uow:
        genre = uow.genres.get_by_id_or_fail(1)

        print("ANTES")
        print("name:", genre.name)
        print("dirty before change:", uow.session.dirty)

        # Mutamos el objeto
        genre.name = genre.name + " (updated)"

        print("\nDESPUÉS DE SETATTR")
        print("dirty after change:", uow.session.dirty)

        # NO llamamos a flush()
        # NO llamamos a repo.update()
        uow.commit()

        print("\nDESPUÉS DEL COMMIT")
        print("dirty after commit:", uow.session.dirty)

if __name__ == "__main__":
    main()