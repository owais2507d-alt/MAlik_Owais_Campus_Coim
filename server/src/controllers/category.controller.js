import { Category } from "../models/Category.js";
import { Transaction } from "../models/Transaction.js";
import { ApiError } from "../utils/apiError.js";
import { asyncHandler } from "../utils/asyncHandler.js";
import { sendSuccess } from "../utils/response.js";
import { notifyUser } from "../services/notify.js";

export const listCategories = asyncHandler(async (req, res) => {
  const { type } = req.query;
  const filter = {
    $or: [{ userId: req.user.id }, { userId: null, isDefault: true }],
  };
  if (type) filter.type = type;

  const categories = await Category.find(filter).sort({ type: 1, name: 1 });

  // de-dupe by (type, name) — a user copy must never shadow a system default twice
  const seen = new Map();
  const deduped = [];
  for (const cat of categories) {
    const key = `${cat.type}:${cat.name.trim().toLowerCase()}`;
    const existing = seen.get(key);
    if (!existing) {
      seen.set(key, cat);
      deduped.push(cat);
    } else if (existing.userId !== null && cat.userId === null) {
      // system default is canonical: replace the personal copy
      seen.set(key, cat);
      deduped[deduped.indexOf(existing)] = cat;
    }
  }

  return sendSuccess(res, { categories: deduped });
});

export const createCategory = asyncHandler(async (req, res) => {
  const { name, type, icon, color } = req.body;
  const trimmed = String(name).trim();
  const escaped = trimmed.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const exists = await Category.findOne({
    $or: [{ userId: req.user.id }, { userId: null, isDefault: true }],
    type,
    name: { $regex: `^${escaped}$`, $options: "i" },
  });
  if (exists) throw ApiError.conflict("Category with this name already exists");

  const category = await Category.create({
    userId: req.user.id,
    name: trimmed,
    type,
    icon: icon || "tag",
    color: color || "#F59E0B",
    isDefault: false,
  });
  await notifyUser(req.user.id, {
    type: "category",
    title: "Category created",
    message: `New ${type} category “${category.name}” is ready to use.`,
  });
  return sendSuccess(res, { category }, "Category created", 201);
});

export const updateCategory = asyncHandler(async (req, res) => {
  const category = await Category.findOne({ _id: req.params.id });
  if (!category) throw ApiError.notFound("Category not found");
  if (category.userId == null) {
    throw ApiError.forbidden("Default categories can't be edited");
  }
  if (String(category.userId) !== req.user.id) throw ApiError.notFound("Category not found");

  const { name, icon, color, type } = req.body;
  if (name) category.name = name;
  if (icon) category.icon = icon;
  if (color) category.color = color;
  if (type) category.type = type;
  await category.save();
  await notifyUser(req.user.id, {
    type: "category",
    title: "Category updated",
    message: `Category “${category.name}” was updated.`,
  });

  return sendSuccess(res, { category }, "Category updated");
});

export const deleteCategory = asyncHandler(async (req, res) => {
  const category = await Category.findOne({ _id: req.params.id });
  if (!category) throw ApiError.notFound("Category not found");
  if (category.userId == null) {
    throw ApiError.forbidden("Default categories can't be deleted");
  }
  if (String(category.userId) !== req.user.id) throw ApiError.notFound("Category not found");

  const count = await Transaction.countDocuments({ userId: req.user.id, categoryId: category._id });
  if (count) {
    throw ApiError.conflict(
      `This category has ${count} transaction${count === 1 ? "" : "s"} — reassign or delete them first`
    );
  }

  await category.deleteOne();
  return sendSuccess(res, null, "Category deleted");
});
