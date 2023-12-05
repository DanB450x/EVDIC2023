function factorial_calculator()
    % Función para calcular el factorial de un número entero
    
    fprintf('Calculadora de Factorial\n');
    fprintf('------------------------\n');
    
    % Pedir al usuario que ingrese un número entero
    num = input('Ingrese un número entero: ');
    
    % Validar que el número sea entero y positivo
    if rem(num, 1) ~= 0 || num < 0
        fprintf('Error: Debe ingresar un número entero no negativo.\n');
        return;
    end
    
    % Calcular el factorial del número ingresado
    factorial_num = factorial(num);
    
    % Mostrar el resultado
    fprintf('El factorial de %d es: %d\n', num, factorial_num);
end