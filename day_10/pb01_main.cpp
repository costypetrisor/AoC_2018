#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>


using GridType = std::array<std::array<int32_t, 300>, 300>;
GridType grid;


void solve_0(size_t serial_number) {
    for (size_t row_idx = 0; row_idx < 300; ++row_idx) {
        for (size_t col_idx = 0; col_idx < 300; ++col_idx) {
            int32_t rack_id = row_idx + 10;
            int32_t power_level = rack_id * col_idx;
            power_level += serial_number;
            power_level *= rack_id;
            power_level = (power_level / 100) % 10;
            power_level -= 5;
            grid[row_idx][col_idx] = power_level;
        }
    }

    size_t max_cell_x = SIZE_MAX, max_cell_y = SIZE_MAX;
    int32_t max_cell_value = INT32_MIN;
    int32_t cell_size = 3;
    for (size_t row_idx = 0; row_idx < 300 - cell_size; ++row_idx) {
        for (size_t col_idx = 0; col_idx < 300 - cell_size; ++col_idx) {
            int32_t cell_value = 0;
            for (size_t i = 0; i < cell_size; ++i) {
                for (size_t j = 0; j < cell_size; ++j) {
                    cell_value += grid[row_idx + i][col_idx + j];
                }
            }
            if (cell_value > max_cell_value) {
                max_cell_x = row_idx;
                max_cell_y = col_idx;
                max_cell_value = cell_value;
            }
        }
    }

    // for (size_t i = std::max(size_t(0U), max_cell_x - 1); i < std::min(size_t(300), max_cell_x + 4); ++i) {
    //     for (size_t j = std::max(size_t(0U), max_cell_y - 1); i < std::min(size_t(300U), max_cell_y + 4); ++j) {
    //         std::cout << grid[i][j] << " ";
    //     }
    //     std::cout << "\n";
    // }

    std::cout << "For serial number " << serial_number << " max_cell(3): " << max_cell_x << "," << max_cell_y << "\n";
}


void solve_1(size_t serial_number) {
    for (size_t row_idx = 0; row_idx < 300; ++row_idx) {
        for (size_t col_idx = 0; col_idx < 300; ++col_idx) {
            int32_t rack_id = row_idx + 10;
            int32_t power_level = rack_id * col_idx;
            power_level += serial_number;
            power_level *= rack_id;
            power_level = (power_level / 100) % 10;
            power_level -= 5;
            grid[row_idx][col_idx] = power_level;
        }
    }

    size_t max_cell_x = SIZE_MAX, max_cell_y = SIZE_MAX, max_cell_size = INT32_MAX;
    int32_t max_cell_value = INT32_MIN;
    int32_t cell_value = INT32_MIN;
    for (int32_t cell_size = 3; cell_size < 301; ++cell_size) {
        cell_value = INT32_MIN;
        for (size_t row_idx = 0; row_idx < 300 - cell_size; ++row_idx) {
            cell_value = INT32_MIN;

            for (size_t col_idx = 0; col_idx < 300 - cell_size; ++col_idx) {
                if (cell_value == INT32_MIN) {
                    cell_value = 0;
                    for (size_t i = 0; i < cell_size; ++i) {
                        for (size_t j = 0; j < cell_size; ++j) {
                            cell_value += grid[row_idx + i][col_idx + j];
                        }
                    }
                } else {
                    for (size_t i = 0; i < cell_size; ++i) {
                        cell_value -= grid[row_idx + i][col_idx - 1];
                        cell_value += grid[row_idx + i][col_idx + cell_size - 1];
                    }
                }
                if (cell_value > max_cell_value) {
                    max_cell_x = row_idx;
                    max_cell_y = col_idx;
                    max_cell_size = cell_size;
                    max_cell_value = cell_value;
                }
            }
        }
    }

    std::cout << "For serial number " << serial_number << " max_cell: " << max_cell_x << "," << max_cell_y << "," << max_cell_size << "\n";
}


int main() {
    solve_1(18);
    solve_1(42);
    solve_1(4172);
    return 0;
}
