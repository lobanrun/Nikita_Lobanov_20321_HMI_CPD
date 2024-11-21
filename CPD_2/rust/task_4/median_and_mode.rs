// Вычисление медианы и моды списка
use std::collections::HashMap;

fn MedianAndMode(list: &mut Vec<i32>) -> (f64, i32) {
    // Отсортируем список по возрастанию
    list.sort();
    
    // Если количество элементов четное
    let median: f64 = if list.len() % 2 == 0 {
        let seredina = list.len() / 2;
        (list[seredina-1] + list[seredina]) as f64 / 2.0
    }
    //  Если количество элементов нечетное
    else {
        list[list.len() / 2] as f64
    };
    
    // Создаем хэш-карту
    let mut map = HashMap::new();
    // Добавляем в хэш-карту значения списка
    for i in list.iter() {
        let mode = map.entry(i).or_insert(0);
        *mode += 1;
    }
    let mut mode = 0;
    let mut max_values = 0;
    
    // Ищем моду списка
    for (&i, &count) in &map {
        if count > max_values {
            max_values = count;
            mode = *i;
        }
    }
    (median, mode)
}

fn main() {
    // Вводим список целых чисел
    let mut list = vec![1,2,2,4,7,9,7,3,3,7];
    let (median, mode) = MedianAndMode(&mut list);
    // Выводим результат
    println!("Median {}", median);
    println!("Mode {}", mode);
}

