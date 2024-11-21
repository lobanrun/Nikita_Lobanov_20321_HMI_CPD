// Поворот изображений
struct Solution;

impl Solution {
    pub fn rotate(matrix: &mut Vec<Vec<i32>>) {
        // Меняем строки местами
        for i in 0..matrix.len() {
            for j in i..matrix.len() {
                let temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
        // Разворачиваем матрицу
        for i in matrix {
            i.reverse();
        }
    }
}

fn main() {
    // Вводим исходную матрицу
    let mut matrix = vec![
    vec![5,1,9,11],
    vec![2,4,8,10],
    vec![13,3,6,7],
    vec![15,14,12,16]];
    // Выводим результат
    Solution::rotate(&mut matrix);
    println!("{:?}", matrix);
}