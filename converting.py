from PIL import Image
import os

def convert_jpeg_to_jpg(folder_path):
    # Проверяем, существует ли указанная папка
    if not os.path.exists(folder_path):
        print(f"Папка '{folder_path}' не существует.")
        return

    # Перебираем файлы в папке
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Проверяем, является ли файл изображением
        if filename.lower().endswith(('.jpeg', '.webp', '.png')):
            try:
                # Открываем изображение
                with Image.open(filepath) as img:
                    # Формируем новое имя файла с расширением .jpg
                    new_filepath = os.path.join(folder_path, os.path.splitext(filename)[0] + '.jpg')

                    # Сохраняем изображение в формате JPG
                    img.convert("RGB").save(new_filepath, 'JPEG')

                # Удаляем старый файл
                os.remove(filepath)

                print(f"Конвертирован файл: {filename} -> {os.path.splitext(filename)[0]}.jpg")
            except Exception as e:
                print(f"Ошибка при конвертации файла {filename}: {e}")
        else:
            print(f"Оставлен без изменений файл: {filename}")


if __name__ == "__main__":
    folder_path = 'saffron_good'

    convert_jpeg_to_jpg(folder_path)
