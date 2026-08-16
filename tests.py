import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

# Тест 1: Установка жанра
def test_set_book_genre_valid_and_invalid(collector):
    collector.add_new_book("Автостопом по галактике")
    
    result_valid = collector.set_book_genre("Автостопом по галактике", "Фантастика")
    assert result_valid is None
    assert collector.get_book_genre("Автостопом по галактике") == "Фантастика"
    
    result_invalid = collector.set_book_genre("Автостопом по галактике", "Романтика")
    assert result_invalid is None
    assert collector.get_book_genre("Автостопом по галактике") == "Фантастика"
    
    # Книга отсутствует в словаре
    assert collector.set_book_genre("Несуществующая книга", "Комедии") is None

# Тест 2: Получение жанра
def test_get_book_genre(collector):
    collector.add_new_book("Дюна")
    collector.set_book_genre("Дюна", "Фантастика") 
    
    genre = collector.get_book_genre("Дюна")
    no_genre = collector.get_book_genre("Книга без жанра")
    
    assert genre == "Фантастика"
    assert no_genre is None

# Тест 3: Поиск книг по конкретному жанру
@pytest.mark.parametrize("genre, books_count", [
    ("Детективы", 1),
    ("Фантастика", 1),
    ("Ужасы", 0)
])
def test_get_books_with_specific_genre(collector, genre, books_count):
    collector.add_new_book("Метро 2033")
    collector.set_book_genre("Метро 2033", "Фантастика")
    
    collector.add_new_book("Шерлок Холмс")
    collector.set_book_genre("Шерлок Холмс", "Детективы")
    
    result = collector.get_books_with_specific_genre(genre)
    assert len(result) == books_count

# Тест 4: Получение всего словаря genres
def test_get_books_genre(collector):
    collector.add_new_book("Книга")
    genres_map = collector.get_books_genre()
    assert isinstance(genres_map, dict)

# Тест 5: Книги для детей
def test_get_books_for_children_excludes_age_rating(collector):
    collector.add_new_book("Король Лев")
    collector.set_book_genre("Король Лев", "Мультфильмы")
    
    collector.add_new_book("Оно")
    collector.set_book_genre("Оно", "Ужасы")
    
    children_books = collector.get_books_for_children()
    assert "Король Лев" in children_books
    assert "Оно" not in children_books

# Тест 6: Добавление в избранное
def test_add_book_in_favorites(collector):
    collector.add_new_book("Трое в лодке, не считая собаки")
    collector.set_book_genre("Трое в лодке, не считая собаки", "Комедии")
    
    collector.add_book_in_favorites("Трое в лодке, не считая собаки")
    assert "Трое в лодке, не считая собаки" in collector.get_list_of_favorites_books()
    
    # Повторное добавление не должно создавать дубликаты
    collector.add_book_in_favorites("Трое в лодке, не считая собаки")
    assert collector.get_list_of_favorites_books().count("Трое в лодке, не считая собаки") == 1

# Тест 7: Удаление из избранного
def test_delete_book_from_favorites(collector):
    collector.add_new_book("Властелин Колец")
    collector.set_book_genre("Властелин Колец", "Фантастика")
    collector.add_book_in_favorites("Властелин Колец")
    
    collector.delete_book_from_favorites("Властелин Колец")
    assert "Властелин Колец" not in collector.get_list_of_favorites_books()

# Тест 8: Список избранного пустой / заполненный
def test_get_list_of_favorites_books_empty_and_filled(collector):
    empty_list = collector.get_list_of_favorites_books()
    assert empty_list == [] # Список пуст до добавления
    
    collector.add_new_book("Зверополис")
    collector.set_book_genre("Зверополис", "Мультфильмы")
    collector.add_book_in_favorites("Зверополис")
    
    filled_list = collector.get_list_of_favorites_books()
    assert filled_list == ["Зверополис"] # После добавления

# Тест 9: Смена жанра
def test_changing_book_genre(collector):
    collector.add_new_book("Нейромант")
    collector.set_book_genre("Нейромант", "Фантастика")
    assert collector.get_book_genre("Нейромант") == "Фантастика"
    
    # Невалидный жанр
    collector.set_book_genre("Нейромант", "Киберпанк")
    assert collector.get_book_genre("Нейромант") == "Фантастика"
    
    # Валидная смена
    collector.set_book_genre("Нейромант", "Детективы")
    assert collector.get_book_genre("Нейромант") == "Детективы"