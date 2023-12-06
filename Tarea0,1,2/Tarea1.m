function calcularFactorial()
    % Pedir al usuario que ingrese un número
    numero = input('Ingrese un número para calcular su factorial: ');

    % Verificar si el número es un entero no negativo
    if floor(numero) == numero && numero >= 0
        % Calcular el factorial del número
        resultado = factorial(numero);
        fprintf('El factorial de %d es %d\n', numero, resultado);
    else
        % Mostrar un mensaje si el número no es un entero no negativo
        fprintf('No se puede calcular el factorial. Ingrese un entero no negativo.\n');
    end
end
