pkg load database

% Configuraci�n de la conexi�n a la base de datos
conn = pq_connect(setdbopts('dbname', 'IVA', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'proyectos'));

% Ingreso del precio del producto
precio = input("Ingrese el precio de su producto: Q");

% C�lculos relacionados con el IVA
IVA = precio * 0.12;
precio_sin_iva = precio - IVA;

fprintf("El precio sin IVA es de Q%0.0f, el IVA es de Q%0.0f\n", precio_sin_iva, IVA);

try
    % Preparar la instrucci�n SQL para la inserci�n
    Ins1 = 'INSERT INTO calculo (ptotal) VALUES (';  % asumiendo que "ptotal" es la columna donde deseas guardar el precio total
    Ins2 = ');';
    Instruccion = strcat(Ins1, num2str(precio), Ins2);

    % Ejecutar la instrucci�n SQL
    pq_exec_params(conn, Instruccion);

catch e
    disp(['Error durante la conexi�n a la DB. Consulte el error: ' e.message]);
end

