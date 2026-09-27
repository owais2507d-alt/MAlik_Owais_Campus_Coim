import "dotenv/config";
import { connectDB } from "../config/db.js";
import { seedSystemCategories } from "./categories.js";
import { seedDemoUsers } from "./users.js";

async function seed() {
  await connectDB();
  await seedSystemCategories();
  await seedDemoUsers();

  console.log("🎉 Seed complete");
  process.exit(0);
}

seed().catch((e) => {
  console.error(e);
  process.exit(1);
});
