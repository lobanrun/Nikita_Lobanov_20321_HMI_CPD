// Емкость с наибольшим количеством воды
struct Solution;

impl Solution {
    pub fn max_area(height: Vec<i32>) -> i32 {
        let mut max_volume = 0; // Максимальный объем воды
        let mut left_border = 0; // Левая граница
        let mut right_border = height.len() - 1; // Правая граница

        while left_border < right_border {
            // Вычисляем текущий объем воды. Ширина * минимальная высота границ
            let current_volume = (right_border - left_border) as i32 * height[left_border].min(height[right_border]);
            // Вычисляем максимальный объем воды 
            max_volume = max_volume.max(current_volume);

            // Сдвигаем границы в сторону увеличения высоты
            if height[left_border] < height[right_border] {
                left_border += 1;
            } else {
                right_border -= 1;
            }
        }

        max_volume // Возвращаем максимальный объем 
    }
}

fn main() {
    let height = vec![1, 8, 6, 2, 5, 4, 8, 3, 7];
    println!("Максимальный объем контейнера: {}", Solution::max_area(height));
}