// Свиная латынь

// Функция для обработки конкретного слова
fn pig_translate(word: &str) -> String {
    // Объявляем список с гласными буквами
    let glas = ['a', 'i', 'e', 'o', 'y'];
    //  Получаем первую букву слова
    let mut first_chat = word.chars().take(1).last().unwrap();
    
    // Если слово начинается с гласной
    if glas.contains(&mut first_chat) {
        // Добавляем -hay в конец слова
        return format!("{}-hay", word);
        }
    // Если слово начинается с согласной
    else {
        let mut chars = word.chars();
        // Получаем первую букву слова
        let first_soglas = chars.next().unwrap();
        // Усекаем первую букву из слова
        let rest_of_word: String = chars.collect();
        return format!("{}-{}ay", rest_of_word, first_soglas);
        }
}

// Построение предложений из переведенных слов
fn get_translated_words(words: &str) -> String {
    let mut translated_words = String::new();
    // Разделяем полученную строку на слова
    for word in words.split_whitespace() {
        // Вызываем функцию для перевода каждого слова
        let translated_pig_word = pig_translate(word);
        // Добавляем переведенное слово в строку
        translated_words.push_str(&translated_pig_word);
        // Разделяем слова пробелами
        translated_words.push(' ');
    }
    translated_words.to_string()
}

fn main() {
    // Вводим строку
    let word = "Hello world";
    // Вызываем функцию
    let translate = get_translated_words(word);
    // Выводим результат
    println!("{}", translate);
}


