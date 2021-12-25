target_area = (235, 259, -118, -62)

if True:
    target_area = (20, 30, -10, -5)


def fx(x0, v0, n):
    n = min(n, v0)
    return x0 + n*v0 - (n-1)*n//2

def step_x(x, vx):
    x += vx
    if vx > 0:
        vx -= 1
    return x, vx


def test_fx():
    x0 = 0
    for v0 in range(100):
        x = 0
        v = v0
        for n in range(100):
            assert fx(x0, v0, n) == x
            x, v = step_x(x, v)

test_fx()


def nx_max(v0):
    return v0

def fx_max(x0, v0):
    return fx(x0, v0, nx_max(v0))


def test_fx_max():
    for v0 in range(100):
        x_old = -1
        x0 = 0
        x = x0
        v = v0
        while x > x_old:
            x_old = x
            x, v = step_x(x, v)

        assert x == fx_max(x0, v0)

test_fx_max()



def fy(y0, v0, n):
    return y0 + n*v0 - (n-1)*n//2

def step_y(y, vy):
    y += vy
    vy -= 1
    return y, vy


def test_fy():
    y0 = 0
    for v0 in range(100):
        y = 0
        v = v0
        for n in range(100):
            assert fy(y0, v0, n) == y
            y, v = step_y(y, v)

test_fy()


def ny_max(y0, v0):
    """
        d/dn y0 + n*v0 - (n-1)*n/2
        = v0 - (n/2 + (n-1)/2)
        = v0 - (n - 1/2)
        = v0 + 0.5 - n

        n0 = v0 + 0.5
    """
    return v0 + 1

def fy_max(y0, v0):
    return fy(y0, v0, nx_max(v0))


def test_fy_max():
    for v0 in range(100):
        y_max = 0
        y_old = 0
        y0 = 0
        y = y0
        v = v0
        while y >= y_old:
            y_old = y
            y, v = step_y(y, v)
            y_max = max(y_max, y)

        assert y_max == fy_max(y0, v0)

test_fy_max()


tx_min, tx_max, ty_min, ty_max = target_area

def hit_x(x):
    return x >= tx_min and x <= tx_max

def hit_y(y):
    return y >= ty_min and y <= ty_max


vx_min = 0
while fx_max(0, vx_min) < tx_min:
    vx_min += 1

vx_max = tx_max

y_max = 0

hit_count = 0

for probe_vx in range(vx_min, vx_max + 1):

    n_max = nx_max(probe_vx)
    n_max_is_hit = hit_x(fx_max(0, probe_vx))

    ns = []
    for n in range(n_max + 1):
        if hit_x(fx(0, probe_vx, n)):
            ns.append(n)

    probe_vy = -1000
    overshot = len(ns) == 0
    buffer = 10
    while not overshot or buffer > 0:
        any_hit = False
        any_leq = False

        for n in ns:
            y = fy(0, probe_vy, n)
            if y <= ty_max:
                any_leq = True

                if y >= ty_min:
                    any_hit = True

        if n_max_is_hit:
            n = n_max
            y = ty_max
            while y >= ty_min:
                y = fy(0, probe_vy, n)
                n += 1

                if hit_y(y):
                    any_leq = True
                    any_hit = True

        if any_hit:
            y_max = max(y_max, fy_max(0, probe_vy))
            hit_count += 1

        overshot = not any_leq
        probe_vy += 1

        if overshot: buffer -= 1

print(y_max, hit_count)


vx = vx_min
vy = 0
n0 = nx_max(vx)

while True:
    any_hit = False

    n = n0
    y = ty_max
    last_y = ty_max
    while y >= ty_min:
        last_last_y = last_y
        last_y = y
        y = fy(0, vy, n)
        n += 1

        if hit_y(y):
            any_hit = True

    print(last_last_y, last_y, y)

    #print(vy, fy(0, vy, n0), any_hit, n - n0)
    assert vy < 10 or any_hit == False

    vy += 1
