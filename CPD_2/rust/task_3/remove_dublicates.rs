// Удаление дубликатов
struct Solution;

impl Solution {
    pub fn remove_duplicates(nums: &mut Vec<i32>) -> i32 {
        // Переменная для подсчета количества уникальных элементов
        let mut uniq_count = 1;
        // Проходимся по элементам массива и проверяем, совпадает ли текущий элемент с предыдущим 
        for i in 1..nums.len() {
            // Если элементы отличаются, добавляем текущий элемент в массив
            if nums[i] != nums[uniq_count - 1] {
                nums[uniq_count] = nums[i];
                // Прибавляем на 1 количество уникальных элементов
                uniq_count += 1;
            }
        }
        // Производим усечение вектора до количества уникальных элементов
        nums.truncate(uniq_count);
        // Возвращаем количество уникальных элемен
        uniq_count as i32 
    }
}

fn main() {
    // Вводим массив целых чисел
    let mut nums = vec![0, 0, 1, 1, 1, 2, 2, 3, 3, 4];
    let expectedNums = Solution::remove_duplicates(&mut nums);
    // Выводим результат
    println!("Количество уникальных элементов в массиве = {}; Массив = {:?}", expectedNums , nums);
}
