using System;
using System.Collections.Generic;
using System.Linq;

namespace Lab03.Rules
{
    public record Fact(string Pred, string A = "", string B = "");

    public class Rule
    {
        public string Name; public int Priority;
        public Func<HashSet<Fact>, bool> Condition; public Action<HashSet<Fact>> Action;
    }

    /// <summary>Forward-chaining движок правил (аналог python/src/rules/engine.py).</summary>
    public class RuleEngine
    {
        public readonly HashSet<Fact> Facts = new();
        public readonly List<Rule> Rules = new();
        public readonly List<string> Log = new();

        public List<string> Run(int maxCycles = 50)
        {
            var fired = new List<string>();
            for (int i = 0; i < maxCycles; i++)
            {
                var before = new HashSet<Fact>(Facts);
                foreach (var r in Rules.OrderByDescending(r => r.Priority))
                    if (r.Condition(Facts)) { r.Action(Facts); fired.Add(r.Name); Log.Add($"{r.Name}: {string.Join(",", Facts)}"); }
                if (Facts.SetEquals(before)) break;
            }
            return fired;
        }
    }
}
