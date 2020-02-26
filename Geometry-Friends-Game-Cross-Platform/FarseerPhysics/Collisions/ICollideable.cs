
namespace FarseerGames.FarseerPhysics.Collisions {
    interface ICollideable<T> {
        void Collide(T t, ContactList contactList);
    }
}
