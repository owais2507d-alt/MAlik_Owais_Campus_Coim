// One-off cleanup: remove personal copies of system default categories.
// Reassigns the user's transactions/budgets to the system category first.
import mongoose from "mongoose";
import { connectDB } from "../config/db.js";
import { Category } from "../models/Category.js";
import { Transaction } from "../models/Transaction.js";
import { Budget } from "../models/Budget.js";

async function main() {
  await connectDB();

  const system = await Category.find({ userId: null, isDefault: true });
  const sysByKey = new Map(
    system.map((c) => [`${c.type}:${c.name.trim().toLowerCase()}`, c])
  );

  const copies = await Category.find({
    userId: { $ne: null },
    isDefault: true,
  });
  console.log(`personal default copies found: ${copies.length}`);

  let reassignedTx = 0;
  let reassignedBudgets = 0;
  let deleted = 0;

  for (const copy of copies) {
    const sys = sysByKey.get(`${copy.type}:${copy.name.trim().toLowerCase()}`);
    if (!sys) {
      // no system twin → keep it (it is effectively a personal default)
      continue;
    }

    reassignedTx += (
      await Transaction.updateMany(
        { userId: copy.userId, categoryId: copy._id },
        { $set: { categoryId: sys._id } }
      )
    ).modifiedCount;

    // budgets: unique per (user, category, month) — move unless one exists
    const budgets = await Budget.find({ userId: copy.userId, categoryId: copy._id });
    for (const b of budgets) {
      const clash = await Budget.exists({
        userId: copy.userId,
        categoryId: sys._id,
        month: b.month,
      });
      if (clash) {
        await b.deleteOne();
      } else {
        b.categoryId = sys._id;
        await b.save();
      }
      reassignedBudgets += 1;
    }

    await copy.deleteOne();
    deleted += 1;
  }

  console.log(
    `done: tx reassigned=${reassignedTx}, budgets handled=${reassignedBudgets}, copies deleted=${deleted}`
  );
  await mongoose.disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
