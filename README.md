# wotr-card-game

Python implementation of the War of the Ring Card Game.

This is a first draft solution. I'm reading through the rule book, implementing
things as I go, with little/no thought given to design. This is so I can
understand the problem. I've discovered many complexities and kinds of
decisions that need to be made that I didn't realise existed before I actually
sat down and tried to write code, see
<https://github.com/kaashif/wotr-card-game/issues/11> for a good example.

Most likely scenario is I shit out some 50% Copilot written code (as I have)
with no design, hack it into a working state, then never rewrite it. Rewriting
it is a pipe dream, but would be nice.

Rewriting in Rust would solve some issues (Python has no macros, no circular
module dependencies, is slow) but introduce others (Do I really care about
aliasing? Also, everything is mutable and effectively global, that's probably
not avoidable).

## Design notes

Originally, the intention was to make something that could be turned into an
OpenAI Gym environment, but I don't think that's easy. It's also not
exactly easy to substitute human opponents in for AIs if you do that.

I think I'll implement the game as if all opponents are humans, making decisions
with e.g. a text prompt.

The AI will then be implemented with some heuristics, e.g.:

* Prefer to cycle/eliminate cards which cannot be played (e.g. we're on path 4,
  cycle cards which can only be played on 1-3).

* Strongly prefer to play cards that increase card draw or carryover limit (e.g.
  Witch-King, Gandalf the White).

* Prefer to use special actions on cards (they're usually good).

* etc

There are also some useful heuristics from the Against the Shadow expansion that
the bot flowchart uses e.g. only playing a card to a battleground if Shadow
could "conceivably win".

## What I'd need to use reinforcement learning

I was effectively trying to implement one of these:
https://pettingzoo.farama.org/environments/classic/hanabi/ for the War of the
Ring Card Game, then use some reinforcement learning algorithms to learn
something good.

I don't think it'll be feasible to use reinforcement learning for this yet until
I've put more thought into:

* How to encode the action space: sometimes weird stuff happens requiring multi
  step actions like using the Palantir, which requires another choice of which
  cards to cycle/eliminate. I'm not really sure what the action space should be,
  like at all.

* How to encode observations about the game state: this isn't that hard but is
  just fiddly.

Once I have my heuristic "AI" implemented, maybe I'll take it further.

## What the actual tedious part is

The tedious part is implementing all of the 120 cards. A lot of them have weird,
non-trivial effects, conditional effects, and even for the ones that don't, I
still have to grind through typing in all of the info about the cards.
