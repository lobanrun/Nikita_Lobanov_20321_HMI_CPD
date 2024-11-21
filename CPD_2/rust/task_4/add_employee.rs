use std::collections::HashMap; 
use std::io;

fn main() { 
    // Создаем пустую хэш-карту для хранения сотрудников по отделам
    let mut company: HashMap<String, Vec<String>> = HashMap::new(); 
    loop { 
        // Бесконечный цикл для обработки пользовательских команд
        println!("Введите команду: (например, \"Добавить Name в Department\" или \"Показать Department\" или \"показать всех\"):");
        // Создаем пустую строку для ввода пользователя
        let mut input = String::new(); 
        // Читаем строку из стандартного ввода
        io::stdin().read_line(&mut input).expect("Не удалось прочитать строку");
        // Удаляем начальные и конечные пробелы из введенной строки
        let input = input.trim(); 

        if input.starts_with("Добавить ") { 
            add_employee(&mut company, input); /
        } else if input.starts_with("Показать ") { /
            show_department(&company, input); 
        } else if input.to_lowercase() == "показать всех" { 
            show_all(&company); 
        }
    }
}

fn add_employee(company: &mut HashMap<String, Vec<String>>, input: &str) {
    // Разбиваем введенную строку на части по пробелам и сохраняем в вектор
    let parts: Vec<&str> = input.split_whitespace().collect(); 
    // Проверяем, что команда содержит достаточно частей (Добавить, Имя, в, Отдел)
    if parts.len() < 4 { 
        println!("Неверный формат команды. Попробуйте снова."); 
        return; 
    }
    // Получаем имя сотрудника из команды
    let name = parts[1]; 
    // Получаем название отдела из команды
    let department = parts[3]; 
    // Получаем или создаем вектор сотрудников для отдела
    let employees = company.entry(department.to_string()).or_insert(Vec::new()); 
    // Добавляем имя сотрудника в вектор
    employees.push(name.to_string()); 

    println!("{} добавлен(а) в отдел {}", name, department); 
}

fn show_department(company: &HashMap<String, Vec<String>>, input: &str) {
    // Разбиваем введенную строку на части по пробелам и сохраняем в вектор
    let parts: Vec<&str> = input.split_whitespace().collect(); 
    // Проверяем, что команда содержит достаточно частей (Показать, Отдел)
    if parts.len() < 2 { 
        println!("Неверный формат команды. Попробуйте снова"); 
        return; 
    }
    // Получаем название отдела из команды
    let department = parts[1]; 
     // Пытаемся получить вектор сотрудников для отдела
    match company.get(department) {
        Some(employees) => {
             // Клонируем вектор сотрудников для сортировки
            let mut sorted_employees = employees.clone();
            sorted_employees.sort(); 
            println!("Сотрудники отдела {}: {:?}", department, sorted_employees); 
        },
        None => println!("Отдел {} не найден", department),
    }
}

fn show_all(company: &HashMap<String, Vec<String>>) {
    // Получаем список всех отделов и сохраняем в вектор
    let mut departments: Vec<&String> = company.keys().collect(); 
    departments.sort(); 
     // Проходим по всем отделам
    for department in departments {
        // Клонируем вектор сотрудников для отдела
        let mut employees = company.get(department).unwrap().clone(); 
        employees.sort(); 
        // Выводим отсортированный список сотрудников отдела
        println!("Отдел {}: {:?}", department, employees); 
    }
}


