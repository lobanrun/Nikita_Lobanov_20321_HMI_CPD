// Азбука Морзе 1
use std::collections::HashMap;

fn morse_translated(code: &str) -> String {
    // Добавляем таблицу Азбуки Морзе  
    let mut morse_code: HashMap<String, String> = HashMap::new();
        morse_code.insert(String::from(".-"), String::from("A"));
        morse_code.insert(String::from("-..."), String::from("B"));
        morse_code.insert(String::from("-.-."), String::from("C"));
        morse_code.insert(String::from("-.."), String::from("D"));
        morse_code.insert(String::from("."), String::from("E"));
        morse_code.insert(String::from("..-."), String::from("F"));
        morse_code.insert(String::from("--."), String::from("G"));
        morse_code.insert(String::from("...."), String::from("H"));
        morse_code.insert(String::from(".."), String::from("I"));
        morse_code.insert(String::from(".---"), String::from("J"));
        morse_code.insert(String::from("-.-"), String::from("K"));
        morse_code.insert(String::from(".-.."), String::from("L"));
        morse_code.insert(String::from("--"), String::from("M"));
        morse_code.insert(String::from("-."), String::from("N"));
        morse_code.insert(String::from("---"), String::from("O"));
        morse_code.insert(String::from(".--."), String::from("P"));
        morse_code.insert(String::from("--.-"), String::from("Q"));
        morse_code.insert(String::from(".-."), String::from("R"));
        morse_code.insert(String::from("..."), String::from("S"));
        morse_code.insert(String::from("-"), String::from("T"));
        morse_code.insert(String::from("..-"), String::from("U"));
        morse_code.insert(String::from("...-"), String::from("V"));
        morse_code.insert(String::from(".--"), String::from("W"));
        morse_code.insert(String::from("-..-"), String::from("X"));
        morse_code.insert(String::from("-.--"), String::from("Y"));
        morse_code.insert(String::from("--.."), String::from("Z"));
        morse_code.insert(String::from("-----"), String::from("0"));
        morse_code.insert(String::from(".----"), String::from("1"));
        morse_code.insert(String::from("..---"), String::from("2"));
        morse_code.insert(String::from("...--"), String::from("3"));
        morse_code.insert(String::from("....-"), String::from("4"));
        morse_code.insert(String::from("....."), String::from("5"));
        morse_code.insert(String::from("-...."), String::from("6"));
        morse_code.insert(String::from("--..."), String::from("7"));
        morse_code.insert(String::from("---.."), String::from("8"));
        morse_code.insert(String::from("----."), String::from("9"));
        morse_code.insert(String::from(".-.-.-"), String::from("."));
        morse_code.insert(String::from("--..--"), String::from(","));
        morse_code.insert(String::from("..--.."), String::from("?"));
        morse_code.insert(String::from(".----."), String::from("'"));
        morse_code.insert(String::from("-.-.--"), String::from("!"));
        morse_code.insert(String::from("-..-."), String::from("/"));
        morse_code.insert(String::from("-.--."), String::from("("));
        morse_code.insert(String::from("-.--.-"), String::from(")"));
        morse_code.insert(String::from(".-..."), String::from("&"));
        morse_code.insert(String::from("---..."), String::from(":"));
        morse_code.insert(String::from("-.-.-."), String::from(";"));
        morse_code.insert(String::from("-...-"), String::from("="));
        morse_code.insert(String::from(".-.-."), String::from("+"));
        morse_code.insert(String::from("-....-"), String::from("-"));
        morse_code.insert(String::from("..--.-"), String::from("_"));
        morse_code.insert(String::from(".-..-."), String::from("\""));
        morse_code.insert(String::from("...-..-"), String::from("$"));
        morse_code.insert(String::from(".--.-."), String::from("@"));
        morse_code.insert(String::from("...---..."), String::from("SOS"));
    
    // Инициализируем переменную для итоговой строки
    let mut res_string = String::new();
    // Разбиваем строки на подстроки, удаляем лишние пробелы 
    let words: Vec<&str> = code.trim().split("  ").collect();

    for word in words {
        // Проходимся по каждому слову
        for morse_character in word.split(" ") {
            if morse_character != "" {
                // Декодируем побуквенно слово
                res_string += morse_code.get(morse_character).unwrap();
            }
        }
        // Добавляем пробел между словами
        res_string.push_str(" ");
    }
    res_string
}

fn main() {
    // Пишем строку на Азбуке Морзе
    let morse_words = ".... . .-.. .-.. ---  .-- --- .-. .-.. -..";
    // Вызываем функцию для декодирования
    let decoded_string = morse_translated(morse_words);
    // Выводим результат
    println!("{}", decoded_string);  
}