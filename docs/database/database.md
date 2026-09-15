## Описание полей таблиц базы данных

Примечание: <br>
Все таблицы наследуются от BaseORM в которой описаны базовые поля
    
    id: int
    created_at: CREATED_AT - кастомная дата
    update_at: UPDATE_AT - кастомная дата

### UsersORM:

    username: Имя пользователя
    email: Email пользователя
    password_hash: Хэш пароль
    role: Роль пользователя
    refresh_tokens: Refresh токен (Связан с таблицей RefreshTokenORM)
    questionnaire: Анета/Профиль (Связана с таблицей QuestionnaireORM)

<hr>

### QuestionnaireORM:

    first_name: Имя
    last_name: Фамилия
    user_id: Ссылка на пользователя 

<hr>

### RefreshTokenORM

    user_id: Ссылка на пользователя
    token_hash: Текущий токен
    expires_at: Время экспирации 
    revoker_at: Время аннулирование

<hr>

### WorksORM
    
    title: Уникальное название
    description: Описание работ 
    price: Цена
    working_hour: Примерное время работ 
    
