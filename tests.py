import pytest
from main import BooksCollector

@pytest.fixture()
def collector():
    return BooksCollector()


# Тесты: Проверка добавления книг
@pytest.mark.parametrize("book_name, expected_result", [
    ("Книга с названием из 40 символов 1234567", True),
    ("A", True),
    ("", False),
    ("Книга с названием из 40 символов 12345678", False) # Превышение лимита (41 символ)
])

def test_add_new_book(collector, book_name, expected_result):
    result = collector.add_new_book(book_name)
    assert (book_name in collector.get_books_genre()) == expected_result

# Тесты: Жанры
def test_set_book_genre_existing_book(collector):
    collector.add_new_book("Автостопом по галактике")
    
    result = collector.set_book_genre("Автостопом по галактике", "Фантастика")
    assert result is None

def test_get_book_genre_existing_book_without_genre(collector):
    collector.add_new_book("Дюна")

    genre = collector.get_book_genre("Дюна") 
    assert genre == ""  # Пустая строка — это валидное значение!

@pytest.mark.parametrize("genre, books_count", [("Детективы", 1)])
def test_get_books_with_specific_genre_positive(collector, genre, books_count):
    collector.add_new_book("Шерлок Холмс")
    collector.set_book_genre("Шерлок Холмс", "Детективы")
    
    result = collector.get_books_with_specific_genre(genre)
    assert len(result) == books_count


@pytest.mark.parametrize("genre, books_count", [("Ужасы", 0)])
def test_get_books_with_specific_genre_negative(collector, genre, books_count):
    result = collector.get_books_with_specific_genre(genre)
    assert len(result) == books_count


@pytest.mark.parametrize("genre, books_count", [("Фантастика", 2)])
def test_get_books_with_specific_genre_multiple(collector, genre, books_count):
    collector.add_new_book("Метро 2033")
    collector.set_book_genre("Метро 2033", "Фантастика")
    
    collector.add_new_book("Гиперион")
    collector.set_book_genre("Гиперион", "Фантастика")
    
    result = collector.get_books_with_specific_genre(genre)
    assert len(result) == books_count


# Тесты: Получение всего словаря genres
def test_get_books_genre_returns_dict(collector):
    collector.add_new_book("Книга")
    genres_map = collector.get_books_genre()

    assert isinstance(genres_map, dict)

#Тесты: Избранное
def test_add_book_in_favorites_single(collector):
    collector.add_new_book("Трое в лодке, не считая собаки")
    collector.add_book_in_favorites("Трое в лодке, не считая собаки")

    assert "Трое в лодке, не считая собаки" in collector.get_list_of_favorites_books()


def test_add_book_in_favorites_no_duplicates(collector):
    collector.add_new_book("Трое в лодке, не считая собаки")
    
    # Первое добавление
    initial_length = len(collector.get_list_of_favorites_books())
    collector.add_book_in_favorites("Трое в лодке, не считая собаки")
    length_after_first_add = len(collector.get_list_of_favorites_books())
    assert length_after_first_add == initial_length + 1

    # Второе повторное добавление
    collector.add_book_in_favorites("Трое в лодке, не считая собаки")
    final_length = len(collector.get_list_of_favorites_books())
    assert final_length == length_after_first_add

def test_delete_book_from_favorites(collector):
    collector.add_new_book("Властелин Колец")
    collector.add_book_in_favorites("Властелин Колец")
    collector.delete_book_from_favorites("Властелин Колец")

    assert "Властелин Колец" not in collector.get_list_of_favorites_books()


def test_get_list_of_favorites_empty(collector):
    empty_list = collector.get_list_of_favorites_books()
    assert empty_list == []

def test_get_list_of_favorites_filled(collector):
    collector.add_new_book("Зверополис")
    collector.add_book_in_favorites("Зверополис")
    
    filled_list = collector.get_list_of_favorites_books()
    assert filled_list == ["Зверополис"]


#Тесты: Книги для детей
def test_get_books_for_children_positive(collector):
    collector.add_new_book("Король Лев")
    collector.set_book_genre("Король Лев", "Мультфильмы")

    children_books = collector.get_books_for_children()
    assert "Король Лев" in children_books


def test_get_books_for_children_negative(collector):
    collector.add_new_book("Оно")
    collector.set_book_genre("Оно", "Ужасы") 

    children_books = collector.get_books_for_children()
    assert "Оно" not in children_books