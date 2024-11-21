// Длина последнего слова в строке
use std::io; 
struct Solution; 

impl Solution {
    pub fn length_of_last_word(s: String) -> usize {
        // Обработка ввода: убираем лишние пробелы и выведем последний введенный элемент    
        let s = match s.trim().split_whitespace().last() { 
            Some(s) => s.len(), 
            None => 0, 
        }; 
        s
    }
}
fn main() { 
    loop {
        // Просим пользователя ввести строку 
        println!("Введите фразу: "); 
        let mut word = String::new(); 
        //  Обработка пользовательского ввода 
        io::stdin().read_line(&mut word) 
                .expect("Failed to read line"); 
        println!("Длина последнего введенного слова: {}", Solution::length_of_last_word(word)); 
    }
}

