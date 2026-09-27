import { User } from "../models/User.js";

const DEMO_USERS = [
  {
    name: "Admin",
    email: "admin@campuscoin.app",
    password: "Admin@123",
    role: "admin",
    currency: "BDT",
  },
  {
    name: "Demo Student",
    email: "demo@campuscoin.app",
    password: "Demo@123",
    role: "student",
    academicYear: "3rd Year",
    allowanceBaseline: 15000,
    savingsGoal: 5000,
    currency: "BDT",
  },
];

export async function seedDemoUsers() {
  for (const u of DEMO_USERS) {
    const exists = await User.findOne({ email: u.email });
    if (exists) continue;

    const user = await User.create({
      ...u,
      password: await User.hashPassword(u.password),
    });
    console.log(`✅ Seeded ${u.role}: ${u.email} / ${u.password}`);
  }
}
