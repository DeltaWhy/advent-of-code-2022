const std = @import("std");
const ArrayList = std.ArrayList;
const test_input = @embedFile("test01.txt");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer _ = gpa.deinit();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);
    if (args.len > 2) {
        std.debug.print("Usage: {s} [file]\n", .{args[0]});
    }

    const f = if (args.len == 2) try std.fs.cwd().openFile(args[1], .{}) else std.io.getStdIn();
    defer f.close();

    const contents = try f.readToEndAlloc(allocator, 1024 * 1024);
    defer allocator.free(contents);
    var data = try parseInput(allocator, contents);
    defer freeData(allocator, data);
    // std.debug.print("{any}\n", .{data});
    const part1 = try solvePart1(allocator, data);
    std.debug.print("{d}\n", .{part1});
    const part2 = try solvePart2(allocator, data);
    std.debug.print("{d}\n", .{part2});
}

const Data = [][]usize;

pub fn freeData(allocator: std.mem.Allocator, data: [][]usize) void {
    for (data) |*item| {
        allocator.free(item.*);
    }
    allocator.free(data);
}

pub fn parseInput(allocator: std.mem.Allocator, input: []const u8) ![][]usize {
    var res = ArrayList([]usize).init(allocator);
    var iter = std.mem.splitScalar(u8, input, '\n');
    var cur_list = ArrayList(usize).init(allocator);
    while (iter.next()) |line| {
        if (std.mem.eql(u8, line, "")) {
            if (cur_list.items.len == 0) continue;
            try res.append(try cur_list.toOwnedSlice());
            cur_list.deinit();
            cur_list = ArrayList(usize).init(allocator);
        } else {
            const val = try std.fmt.parseInt(usize, line[0..line.len], 10);
            try cur_list.append(val);
        }
    }
    if (cur_list.items.len == 0) {
        cur_list.deinit();
    } else {
        try res.append(try cur_list.toOwnedSlice());
        cur_list.deinit();
    }
    return res.toOwnedSlice();
}

pub fn solvePart1(allocator: std.mem.Allocator, data: Data) !usize {
    var sums: []usize = try allocator.alloc(usize, data.len);
    defer allocator.free(sums);
    for (data, 0..) |list, i| {
        sums[i] = 0;
        for (list) |x| {
            sums[i] += x;
        }
    }
    var max: usize = 0;
    for (sums) |sum| {
        max = @max(max, sum);
    }
    return max;
}

test "test part 1" {
    var data = try parseInput(std.testing.allocator, test_input);
    defer freeData(std.testing.allocator, data);
    var res = try solvePart1(std.testing.allocator, data);
    try std.testing.expectEqual(res, 24000);
}

pub fn solvePart2(allocator: std.mem.Allocator, data: Data) !usize {
    var sums: []usize = try allocator.alloc(usize, data.len);
    defer allocator.free(sums);
    for (data, 0..) |list, i| {
        sums[i] = 0;
        for (list) |x| {
            sums[i] += x;
        }
    }
    std.sort.heap(usize, sums, {}, std.sort.desc(usize));
    std.debug.assert(sums.len >= 3);
    return sums[0] + sums[1] + sums[2];
}

test "test part 2" {
    var data = try parseInput(std.testing.allocator, test_input);
    defer freeData(std.testing.allocator, data);
    var res = try solvePart2(std.testing.allocator, data);
    try std.testing.expectEqual(res, 45000);
}
