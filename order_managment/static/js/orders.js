// Получение CSRF-токена
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Создание нового заказа
document.addEventListener('DOMContentLoaded', () => {
    const createForm = document.getElementById('create-order-form');
    if (createForm) {
        createForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const selectedDishes = Array.from(document.getElementById('items').selectedOptions);
            const dishes = selectedDishes.map(option => option.value);

            const data = {
                table_number: document.getElementById('table_number').value,
                items: dishes,
            };

            const response = await fetch('/api/orders/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(data),
            });

            const responseData = await response.json();

            if (response.ok) {
                if (responseData.redirect) {
                    console.log(responseData.redirect);
                    window.location.href = responseData.redirect;
                }
            } else {
                alert('Ошибка при создании заказа');
            }
        });

        // Автоматический расчет суммы при выборе блюд
        document.getElementById('items').addEventListener('change', function () {
            let totalPrice = 0;
            Array.from(this.selectedOptions).forEach(option => {
                totalPrice += parseFloat(option.dataset.price);
            });
            document.getElementById('total_price').value = totalPrice.toFixed(2);
        });
    }

    // Загрузка списка заказов
    const loadOrders = async (query = '') => {
        const url = query ? `/api/orders/?search=${query}` : '/api/orders/';
        const response = await fetch(url);
        const orders = await response.json();
        const tbody = document.querySelector('#order-table tbody');
        tbody.innerHTML = '';
        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.table_number}</td>
                <td>${order.items.map(item => item.name).join(', ')}</td>
                <td>${order.total_price}</td>
                <td>
                    <select class='status-select' data-order-id='${order.id}'>
                        <option value='waiting' ${order.status === 'waiting' ? 'selected' : ''}>В ожидании</option>
                        <option value='ready' ${order.status === 'ready' ? 'selected' : ''}>Готов</option>
                        <option value='paid' ${order.status === 'paid' ? 'selected' : ''}>Оплачено</option>
                    </select>
                </td>
                <td>
                    <button class="delete-btn" data-order-id="${order.id}">Удалить</button>
                </td>
            `;
            tbody.appendChild(row);
        });

        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                const orderId = e.target.dataset.orderId;
    
                const confirmed = confirm('Вы уверены, что хотите удалить этот заказ?');
                if (!confirmed) return;
    
                const response = await fetch(`/api/orders/${orderId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                });
    
                if (response.ok) {
                    alert('Заказ успешно удалён');
                    loadOrders(); // Обновляем список заказов после удаления
                } else {
                    alert('Ошибка при удалении заказа');
                }
            });
        });

        // Обработчик изменения статуса заказа
        document.querySelectorAll('.status-select').forEach(select => {
            select.addEventListener('change', async (e) => {
                const orderId = e.target.getAttribute('data-order-id');
                const newStatus = e.target.value;

                const response = await fetch(`/api/orders/${orderId}/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ status: newStatus }),
                });

                if (!response.ok) {
                    alert('Ошибка при обновлении статуса');
                }
            });
        });
    };
    // Обработка поиска
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');

    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim();
        loadOrders(query);
    });

    // Загрузка списка заказов при наличии таблицы
    if (document.getElementById('order-table')) {
        loadOrders();
    } else {
        console.error('Таблица заказов не найдена');
    }

    // Обработчик для кнопки выручки
    const revenueBtn = document.getElementById('revenue-btn');
    if (revenueBtn) {
        revenueBtn.addEventListener('click', async () => {
            const revenueResponse = await fetch('/api/orders/revenue/');
            const data = await revenueResponse.json();
            const revenueAmount = document.getElementById('revenue-amount');
            revenueAmount.textContent = data.revenue;
            document.getElementById('revenue-display').style.display = 'block';
        });
    }
});
