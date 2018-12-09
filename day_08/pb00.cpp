#include <algorithm>
#include <iostream>
#include <list>
#include <vector>
#include <map>


uint64_t solve(uint64_t nb_player, uint64_t max_marble) {
    std::map<uint64_t, uint64_t> score_table;

    std::list<uint64_t> circle;
    circle.push_back(0U);
    circle.push_back(1U);
    int64_t last_marble_idx = 1;
    std::list<uint64_t>::iterator last_marble_it = circle.begin();
    std::advance(last_marble_it, last_marble_idx);

    int64_t player = -1;

    for (uint64_t marble = 2; marble < max_marble + 1; ++marble) {
        player += 1;
        player %= nb_player;

        bool is_23_multiple = (marble % 23) == 0;

        if (is_23_multiple) {
            int64_t old_marble_idx = last_marble_idx;
            last_marble_idx -= 7;
            while (last_marble_idx < 0) {
                last_marble_idx += circle.size();
            }
            if (last_marble_idx < old_marble_idx) {
                std::advance(last_marble_it, -7);
            } else {
                std::list<uint64_t>::iterator old_marble_it = last_marble_it;
                last_marble_it = circle.end();
                int64_t diff = -7 + std::distance(circle.begin(), old_marble_it);
                std::advance(last_marble_it, diff);
            }
            // std::cout << "last_marble_idx=" << last_marble_idx << " circle.size=" << circle.size() << " last_marble_it_dist=" << std::distance(circle.begin(), last_marble_it) << '\n';

            uint64_t marble_removed = *last_marble_it;
            last_marble_it = circle.erase(last_marble_it);
            if (last_marble_it == circle.end()) {
                last_marble_it = circle.begin();
            }
            score_table[player] += marble + marble_removed;
        } else {
            int64_t new_marble_idx = (last_marble_idx + 2) % circle.size();
            std::advance(last_marble_it, 1);
            if (last_marble_it == circle.end()) {
                last_marble_it = circle.begin();
            }
            std::advance(last_marble_it, 1);
            if (last_marble_it == circle.end()) {
                last_marble_it = circle.begin();
            }

            last_marble_it = circle.insert(last_marble_it, marble);
            last_marble_idx = new_marble_idx;

            // std::cout << "last_marble_idx=" << last_marble_idx << " circle.size=" << circle.size() << " last_marble_it_dist=" << std::distance(circle.begin(), last_marble_it) << '\n';
        }

        // if (max_marble > 70000) {
        //     if (marble % 70000 == 0) {
        //         std::cout << "Progress: " << marble / 70000 << "\n";
        //     }
        // }
    }

    std::vector<std::pair<uint64_t, uint64_t>> points_to_player;
    for (const auto& kv : score_table) {
        points_to_player.emplace_back(std::pair<uint64_t, uint64_t>{kv.first, kv.second});
    }
    sort(points_to_player.begin(), points_to_player.end(), [](std::pair<uint64_t, uint64_t> a, std::pair<uint64_t, uint64_t> b) {
        return a.second > b.second;
    });

    //
    // for (const auto& pp : points_to_player) {
    //     std::cout << '\t' << pp.first << ' ' << pp.second << '\n';
    // }
    //
    return points_to_player[0].second;
}


int main() {
    struct Test {
        uint64_t nb_players;
        uint64_t max_marble;
        uint64_t expected;
    };
    std::vector<Test> tests{
        {9, 25, 32, },
        {10, 1618, 8317, },
        {13, 7999, 146373, },
        {17, 1104, 2764, },
        {21, 6111, 54718, },
        {30, 5807, 37305, },
        {458, 71307, 0},
        {458, 71307 * 100, 0},
    };
    for (const auto& test : tests) {
        uint64_t result = solve(test.nb_players, test.max_marble);
        std::cout << "For nb_player=" << test.nb_players
            << " max_marble=" << test.max_marble
            << " expected=" << test.expected << "   result=" << result << '\n';
    }
    return 0;
}

