// Самый длинный общий префикс
struct Solution;

impl Solution {
    pub fn longest_common_prefix(strs: Vec<String>) -> String {
        // С помощью итератора получаем минимальную длину из всех строк
        let min_length = strs.iter().map(|s| s.len()).min().unwrap();

        for i in 0..min_length {
            // Получаем байтовое значение символа 
            let chr = strs[0].as_bytes()[i];

            for j in 1..strs.len() {
                if strs[j].as_bytes()[i] != chr {
                    return strs[0][..i].to_string(); // Если буквы не совпадают, возвращаем префикс
                }
            }
        }
        // Если все символы совпадают, то возвращаем клон первого слова
        strs[0].clone()
    }
}
fn main() {
    let strings = vec!["dollar".to_string(), "dolphin".to_string(), "dolby".to_string()]; 
    println!("{}", Solution::longest_common_prefix(strings));
}