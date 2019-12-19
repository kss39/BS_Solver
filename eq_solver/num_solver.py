import numpy as np

tau = 1 / 255


def u(data_block):
    """Find the quadratic approximation of u_a, u_b on the given day.

    Parameters
    ----------
    data_block : ndarray
        The block of data.

    Returns
    -------
    (u_a, u_b) : (poly1d, poly1d)
        The equations for u_a and u_b.
    """
    ask_data = data_block.iloc[0:3, 2:3].values.squeeze()
    bid_data = data_block.iloc[0:3, 3:4].values.squeeze()
    ask_fit = np.polyfit([-2 * tau, -1 * tau, 0], ask_data, 2)
    bid_fit = np.polyfit([-2 * tau, -1 * tau, 0], bid_data, 2)
    u_a = np.poly1d(ask_fit, variable='t')
    u_b = np.poly1d(bid_fit, variable='t')
    return u_a, u_b


def sigma(data_block):
    """Find the volatility sigma on the given day.

    Similar to u(date_index).

    Parameters
    ----------
    date_index : int
        The index of the date for fitting

    Returns
    -------
    sigma : poly1d
        The equation for volatility.
    """
    vola_data = data_block.iloc[0:3, 7:8].values.squeeze()
    vola_fit = np.polyfit([-2 * tau, -1 * tau, 0], vola_data, 2)
    out = np.poly1d(vola_fit, variable='t')
    return out


def find_sab(data_block):
    """Returns the sa, sb value at the given day.
    """
    s_a = data_block.iloc[2, 5]
    s_b = data_block.iloc[2, 6]
    return s_a, s_b


def find_ax(s_a, s_b):
    """Returns a function evaluating A(x) on the given day.
    """
    diff = s_a - s_b
    return lambda x: (255 / 2) * (((x * diff) + s_b) ** 2) / (diff ** 2)


def initial_value(ua, ub):
    """Returns the initial value at u(x, 0).
    """
    return lambda x: (ua - ub) * x + ub


def system_af(u_a, u_b, a_x, vola, initial, m):
    """Returns the matrix A generated by all conditions.

    Parameters
    ----------
    u_a : numpy.poly1d
        option ask price function

    u_b : numpy.poly1d
        option bid price function

    a_x : double -> double
        A(x)

    vola : numpy.poly1d
        sigma(x)

    initial : double -> double
        initial value

    m : int
        M,N value (grid_count)
        Notice that grid_count > 2.

    Returns
    -------
    the matrix A and the vector f
    """
    matrix = []
    f = []

    h_x = 1 / m
    h_t = 3 * tau / m

    for i in range(m - 1):  # 0 to (M - 2)
        for j in range(1, m - 1):  # 1 to (M - 2)
            Ax = a_x(j * h_x)
            sigma2 = np.polyval(vola, i * h_x) ** 2
            row = np.zeros(m ** 2)
            row[i * m + j] = (h_x ** 2 - 2 * sigma2 * Ax * h_t)
            row[i * m + j - m] = - h_x ** 2
            row[i * m + j + 1] = sigma2 * Ax * h_t
            row[i * m + j - 1] = sigma2 * Ax * h_t
            matrix.append(row)
            f.append(0.0)

    for i in range(m - 1):
        row_a = np.zeros(m ** 2)
        row_b = np.zeros(m ** 2)
        row_init = np.zeros(m ** 2)
        row_a[i] = 1
        matrix.append(row_a)
        f.append(np.polyval(u_a, (i * h_t)))
        row_b[i] = 1
        matrix.append(row_b)
        f.append(np.polyval(u_b, (i * h_t)))
        row_init[i] = 1
        matrix.append(row_init)
        f.append(initial(i * h_x))

    return matrix, f


def tikhonov(matrix, f, beta):
    matrix_trans = np.transpose(matrix)
    right = np.matmul(matrix_trans, f)
    left = np.linalg.inv(np.add(np.matmul(matrix_trans, matrix), beta * np.identity(len(matrix[0]))))
    return np.matmul(left, right)
