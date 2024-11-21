// Слияние отсортированного массива
struct Solution;
impl Solution {
    pub fn merge(nums1: &mut Vec<i32>, m: i32, nums2: &mut Vec<i32>, n: i32) {
        // Выполняем усечение массивов согласно их размеру
        nums1.truncate(m as usize);
        nums2.truncate(n as usize);
        // Выполняем слияние
        nums1.append(nums2); 
        // Сортируем массив
        nums1.sort();
    }
}

fn main() { 
    // Вводим первый массив   
    let mut nums1 = vec![1,2,3,0,0,0];
    // Вводим размер первого массива
    let m = 3;
    // Вводим второй массив
    let mut nums2 = vec![2,5,6];
    // Вводим размерность второго массива
    let n = 4;
    // Вызываем функцию для слияния в единый массив
    let sln = Solution::merge(&mut nums1, m, &mut nums2, n); 
    println!("{:?}", nums1);
}