from services.google import search_places_nearby


if __name__ == '__main__':
    my_location = '43.238949,76.889709'  # координаты Алматы
    results = search_places_nearby(my_location, place_type='cafe', radius=1000)

    if results:
        print("🔍 Найдено:")
        for place in results:
            print(f"• {place}")
    else:
        print("Ничего не найдено.")