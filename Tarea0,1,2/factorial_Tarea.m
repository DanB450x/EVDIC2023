function factorial_calculator()
    % Funci�n para calcular el factorial de un n�mero entero
    
    fprintf('Calculadora de Factorial\n');
    fprintf('------------------------\n');
    
    % Pedir al usuario que ingrese un n�mero entero
    num = input('Ingrese un n�mero entero: ');
    
    % Validar que el n�mero sea entero y positivo
    if rem(num, 1) ~= 0 || num < 0
        fprintf('Error: Debe ingresar un n�mero entero no negativo.\n');
        return;
    end
    
    % Calcular el factorial del n�mero ingresado
    factorial_num = factorial(num);
    
    % Mostrar el resultado
    fprintf('El factorial de %d es: %d\n', num, factorial_num);
end