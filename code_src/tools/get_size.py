
def get_size(parent_width, parent_height, self_ratio, max_x_percent=1, max_y_percent=1):
    parent_width *= max_x_percent
    parent_height *= max_y_percent
    coef = min(
        parent_width / self_ratio,
        parent_height,
    )
    w = coef * self_ratio
    h = coef
    return w, h


if __name__ == '__main__':
    print(get_size(10, 10, 2))
