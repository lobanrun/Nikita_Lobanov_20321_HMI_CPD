// Конвертер температур
use std::io;

fn main() {
    loop {
        println!("Введите температуру в градусах Цельсия");
        //  Создаем переменную для хранения введенного значения
        let mut temperature = String::new();
        
        //  Обрабатываем пользовательский ввод
        io::stdin()
            .read_line(&mut temperature)
            .expect("Failed to read line");

        // Обработка недопустимого ввода
        let temperature: u32 = match temperature.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
        // Конвертируем градусы Цельсия в Фаренгейты
        let Farengeith: u32 = temperature*9/5+32;

        //  Выводим результат
        println!("Температура в Фаренгейтах: {Farengeith}");
        }
}