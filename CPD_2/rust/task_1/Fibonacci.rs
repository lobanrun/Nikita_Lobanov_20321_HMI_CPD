// Числа Фибоначчи
use std::io;

// Функция для вычисления ряда Фибоначчи
fn fibonachi(n: u32) -> u64 {
    // Первое число
    if n == 0 {
        return 0;
    // Второе число
    } else if n == 1 {
        return 1;
    // Расчет последующих чисел
    } else {
        let mut a = 0;
        let mut b = 1;
        let mut result = 0;
        
        for _ in 2..=n {
            result = a + b;
            a = b;
            b = result;
        }
        return result;
    }
}

fn main() {
    loop {
        //  Создаем переменную для хранения введенного числа Фибоначчи
        println!("Введите количество чисел для вычисления ряда Фибоначчи");
        let mut n = String::new();

        //  Обработка пользовательского ввода
        io::stdin()
            .read_line(&mut n)
            .expect("Failed to read line");

        // Обработка недопустимого ввода    
        let n: u32 = match n.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,};
        // Вывод ряда Фибоначчи      
        for i in 0..n{
            println!("F({}) = {}", i, fibonachi(i));
        }
    }
}
