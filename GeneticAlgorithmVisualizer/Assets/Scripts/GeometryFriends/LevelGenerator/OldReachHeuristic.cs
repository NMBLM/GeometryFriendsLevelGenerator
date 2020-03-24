using System;
using System.Collections.Generic;
using System.Drawing;
using UnityEngine;

namespace GeometryFriends.LevelGenerator
{
    public class OldReachHeuristic
    {
        public class Cell
        {
            public PlatformType Platform = PlatformType.NotPlatform;
            public bool fitsRectangle = false;
            public bool fitsCircle = false;
            public bool reachesRectangle = false;
            public bool traversedRectangleLeft = false;
            public bool traversedRectangleRight = false;
            public bool reachesCircle = false;
            public bool traversedCircleLeft = false;
            public bool traversedCircleRight = false;
            public int jumpStrength = 0;
            //public bool cooperativeExclusive;
        }
        public float blockSize;
        public Cell[,] cellGrid;
        public BlockType[,] grid;
        public int xGridLen, yGridLen;
        
        public int circleLen;

        public int rectangleStartLen, rectangleMinLen, rectangleMaxLen;
        //Common Factors for 1200 and 720 are The common factors are:
        //blockSize:   1,  2,  3,  4,  5,  6,  8, 10, 12, 15, 16, 20, 24, 30, 40, 48, 60, 80,120,240
        //xGridLen: 1200,600,400,300,240,200,150,120,100, 80, 75, 60, 50, 40, 30, 25, 20, 15, 10,  5
        //yGridLen: 720 ,360,240,180,144,120, 90, 72, 60, 48, 45, 36, 30, 24, 18, 15, 12,  9,  6,  3
        
        //Circle takes 80x80
        //Rectangle takes 100x100 min/max 50x200 or 200x50.
        //NumOfBlocks for Circle:
        // 80, 40,-,20,16,-,10, 8,-,-,5, 4,-,-,2,-,-,1,-,-
        //NumOfBlocks for Rectangle: 
        //100, 50,-,25,20,-, -,10,-,-,-, 5,-,-,-,-,-,-,-,-
        // 50, 25,-, -,10,-, -, 5,-,-,-, -,-,-,-,-,-,-,-,-
        //200,100,-,50,40,-,25,20,-,-,-,10,-,-,5,-,-,-,-,-
        
        public OldReachHeuristic( float blockSize = 20f)
        {
            //For now fix in BlockSize in 20 so 60x, 36y
            //Circe is 4x4
            //Rectangle is 5x5 or 2.5x10 or 10x2.5
            this.blockSize = 16f;
            // + 4 because always two lines of platforms all around
            xGridLen = (int) ((1240 - 40) / this.blockSize + 0.5f) + 4; // +0.5f to round up;
            yGridLen = (int) ((760 - 40) / this.blockSize + 0.5f) + 4; // +0.5f to round up;

            circleLen = (int) (80 / this.blockSize + 0.5f);
            rectangleStartLen = (int) (100 / this.blockSize + 0.5f);
            rectangleMinLen = (int) (50 / this.blockSize +0.5f); 
            rectangleMaxLen = (int) (200 / this.blockSize + 0.5f);
            
            /** /
            Debug.Log("xGridLen: " + xGridLen + " yGridLen: " + yGridLen);
            Debug.Log("circleLen: " + circleLen);
            Debug.Log("rectangleStartLen: "+ rectangleStartLen + " rectangleMinLen: " + rectangleMinLen + " rectangleMaxLen: " + rectangleMaxLen);
            /**/
            
            cellGrid = new Cell[xGridLen,yGridLen];
        }
        
        public float CalculateFitness(LevelDNA level)
        {
            InitGrid(level);
            Debug.Log("Calcfits");
            InitFits();
            Debug.Log("CalcRecReach");
            RectangleReachability(level);
            Debug.Log("CalcCircReach");
            CircleReachability(level);
            CellGridToBlockGrid();
            return 0;
        }

        public void InitGrid(LevelDNA level)
        {
            for (int i = 0; i < xGridLen; i++)
            {
                for (int j = 0; j < yGridLen; j++)
                {
                    
                    cellGrid[i,j] = new Cell();
                    if (i == 0 || i == xGridLen - 1 || i == 1 || i == xGridLen - 2)
                    {
                        cellGrid[i, j].Platform = PlatformType.Common;
                    }
                    if (j == 0 || j == yGridLen - 1 || j == 1 || j == yGridLen - 2)
                    {
                        cellGrid[i, j].Platform = PlatformType.Common;
                    }
                    
                }
            }
            foreach (var plat in level.platforms)
            {
                int platPosX = (int) ((plat.position.X - 40) / this.blockSize) + 2;
                int platPosY = (int) ((plat.position.Y - 40) / this.blockSize) + 2;
                int platWidth = (int) (plat.width / this.blockSize + 0.5f);
                int platHeight = (int) (plat.height / this.blockSize + 0.5f);

                if (platPosX > xGridLen || platPosY > yGridLen)
                {
                    Debug.Log("Bad platform positioning (" + plat.position.X + " , " + plat.position.Y + ")");
                }

                for (int i = platPosX; i < (platPosX + platWidth) && i < xGridLen; i++)
                {
                    for (int j = platPosY; j < (platPosY + platHeight) && j < yGridLen; j++)
                    {
                        switch (plat.platformType)
                        {
                            case PlatformType.Common:
                                cellGrid[i, j].Platform = PlatformType.Common;
                                break;
                            case PlatformType.CirclePlatform:
                                cellGrid[i, j].Platform = PlatformType.CirclePlatform;
                                break;
                            case PlatformType.RectanglePlatform:
                                cellGrid[i, j].Platform = PlatformType.RectanglePlatform;
                                break;
                        }
                    }
                }
            }
        }

        public void InitFits()
        {
            //Start at 2, end at -2 to ignore boundary
            for (int x = 2; x < xGridLen-2; x++)
            {
                for (int y = 2; y < yGridLen-2; y++)
                {
                    var stillFitRectangle = true;
                    var stillFitCircle = true;

                    for (int i = -1; i <= 1 && stillFitRectangle; i++)
                    {
                        for (int j = -1; j <= 1 && stillFitRectangle; j++)
                        {
                            if (cellGrid[x+i, y+j].Platform != PlatformType.NotPlatform)
                            {
                                stillFitRectangle = false;
                            }
                        }
                    }
                    for (int i = -2; i <= 2 && stillFitCircle; i++)
                    {
                        for (int j = -2; j <= 2 && stillFitCircle; j++)
                        {
                            if (cellGrid[x+i, y+j].Platform != PlatformType.NotPlatform)
                            {
                                stillFitCircle = false;
                            }
                        }
                    }
                    if (stillFitRectangle)
                    {
                        cellGrid[x, y].fitsRectangle = true;
                    }
                    if (stillFitCircle)
                    {
                        cellGrid[x, y].fitsCircle = true;
                    }
                }
            }
        }

        public void RectangleReachability(LevelDNA level)
        {
            //plus 3 because boundary and to center
            int x = (int) ((level.rectangleSpawn.position.X - 40) / this.blockSize) + 3;
            int y = (int) ((level.rectangleSpawn.position.Y - 40) / this.blockSize) + 3;
            List<Tuple<Point,int>> list = new List<Tuple<Point,int>>();
            list.Add(new Tuple<Point,int>(new Point(x, y),0));
            while (list.Count > 0)
            {
                var startPos = list[0];
                x = startPos.Item1.X;
                y = startPos.Item1.Y;
                var dir = startPos.Item2;
                list.RemoveAt(0);
                if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
                {
                    continue;
                }
                if (cellGrid[x, y].reachesRectangle)
                {
                    if (dir == -1)
                    {
                        if (!cellGrid[x, y].traversedRectangleLeft)
                        {
                            cellGrid[x, y].traversedRectangleLeft = true;
                        }
                        else
                        {
                            continue;
                        }
                    }
                    else if (dir == 1)
                    {
                        if (!cellGrid[x, y].traversedRectangleRight)
                        {
                            cellGrid[x, y].traversedRectangleRight = true;
                        }
                        else
                        {
                            continue;
                        }
                    }
                    else
                    {
                        continue;
                    }
                }
                if (cellGrid[x, y].fitsRectangle)
                {
                    cellGrid[x, y].reachesRectangle = true;
                    switch (dir)
                    {
                        case -1:
                            cellGrid[x, y].traversedRectangleLeft = true;
                            break;
                        case 1:
                            cellGrid[x, y].traversedRectangleRight = true;
                            break;
                    }
                    //Check if Falling
                    if (cellGrid[x, y + 1].fitsRectangle)
                    {
                        list.Add(new Tuple<Point,int>(new Point(x, y+1),dir));
                        switch (dir)
                        {
                            case -1:
                                cellGrid[x, y].traversedRectangleLeft = true;
                                list.Add(new Tuple<Point, int>(new Point(x + dir, y + 1), dir));
                                break;
                            case 1:
                                cellGrid[x, y].traversedRectangleRight = true;
                                list.Add(new Tuple<Point, int>(new Point(x + dir, y + 1), dir));
                                break;
                        }
                        continue;
                    }

                    
                    //Check for going left
                    if (cellGrid[x - 1, y].fitsRectangle)
                    {
                        list.Add(new Tuple<Point,int>(new Point(x-1, y),-1));
                        for (int i = 0; i < rectangleMaxLen; i++) //extend
                        {
                            list.Add(new Tuple<Point,int>(new Point(x-1, y-i),0));
                        }
                    }
                    else
                    {
                        for (int i = 0; i < 3; i++)
                        {
                            list.Add(new Tuple<Point,int>(new Point(x-1, y-i),-1));
                        }
                    }
                    //Check for going right
                    if (cellGrid[x + 1, y].fitsRectangle)
                    {
                        list.Add(new Tuple<Point,int>(new Point(x+1, y),1));
                        for (int i = 0; i < rectangleMaxLen; i++) //extend
                        {
                            list.Add(new Tuple<Point,int>(new Point(x+1, y-i),0));
                        };
                    }else
                    {
                        for (int i = 0; i < 3; i++)
                        {
                            list.Add(new Tuple<Point,int>(new Point(x+1, y-i),1));
                        }
                    }
                }
                
            }
           
        }

         public void CircleReachability(LevelDNA level)
        {
            //plus 3 because boundary and to center
            int x = (int) ((level.circleSpawn.position.X - 40) / this.blockSize) + 4;
            int y = (int) ((level.circleSpawn.position.Y - 40) / this.blockSize) + 4;
            int cellsChecked = 0;
            int freefalling = 0;
            List<Tuple<Point,int>> list = new List<Tuple<Point,int>>();
            list.Add(new Tuple<Point,int>(new Point(x, y),0));
            while (list.Count > 0 && cellsChecked < 10000)
            {
                cellsChecked += 1;
                var startPos = list[0];
                x = startPos.Item1.X;
                y = startPos.Item1.Y;
                var dir = startPos.Item2;
                list.RemoveAt(0);
                if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
                {
                    continue;
                }

                if (cellGrid[x, y].jumpStrength == 24)
                {
                    continue;
                }
                /**/
                if (cellGrid[x, y].fitsCircle)
                {
                    cellGrid[x, y].reachesCircle = true;
                    //Check On the Ground
                    if (!cellGrid[x, y + 1].fitsCircle)
                    {
                        cellGrid[x, y].jumpStrength = 24;

                        if (cellGrid[x - 1, y].jumpStrength < 24)
                        {
                            list.Add(new Tuple<Point, int>(new Point(x - 1, y), -1));
                        }

                        if (cellGrid[x + 1, y].jumpStrength < 24)
                        {
                            list.Add(new Tuple<Point, int>(new Point(x + 1, y), 1));
                        }

                        for (int i = -1; i < 1; i++)
                        {
                            if (cellGrid[x + i, y - 1].jumpStrength < 23)
                            {
                                cellGrid[x + i, y - 1].jumpStrength = 23;
                                list.Add(new Tuple<Point, int>(new Point(x + i, y - 1), i));
                            }
                        }
                    }
                    /**/
                    /**/
                    else // Mid-air
                    {
                        /**/
                        //if mid jump
                        if (cellGrid[x, y].jumpStrength > 0 && cellGrid[x, y].jumpStrength < 24)
                        {
                            for (int j = -1; j <= 1; j++)
                            {

                                if (cellGrid[x + j, y - 1].jumpStrength < cellGrid[x, y].jumpStrength - 1)
                                {
                                    
                                    cellGrid[x + j, y - 1].jumpStrength = cellGrid[x, y].jumpStrength - 1;
                                    list.Add(new Tuple<Point, int>(new Point(x + j, y - 1), dir));
                                }
                            }

                            if (cellGrid[x, y].jumpStrength - 1 == 0)
                            {
                                list.Add(new Tuple<Point, int>(new Point(x + dir, y), dir));
                            }
                        }
                        else // free fall
                        /**/
                        {
                            freefalling += 1;
                            list.Add(new Tuple<Point,int>(new Point(x, y+1),0));
                            switch (dir)
                            {
                                case -1:
                                    cellGrid[x, y].traversedCircleLeft = true;
                                    list.Add(new Tuple<Point, int>(new Point(x + dir, y + 1), dir));
                                    break;
                                case 1:
                                    cellGrid[x, y].traversedCircleRight = true;
                                    list.Add(new Tuple<Point, int>(new Point(x + dir, y + 1), dir));
                                    break;
                            }
                        }
                       
                    }
                    /**/
                }

            }
            Debug.Log(list.Count +" ; "+ cellsChecked + " : "+ freefalling);
        }

         public bool TmpFunc(int x, int y, int dir)
         {
             
             /**/
             if (cellGrid[x, y].reachesCircle)
             {
                 if (dir == -1)
                 {
                     if (!cellGrid[x, y].traversedCircleLeft)
                     {
                         cellGrid[x, y].traversedCircleLeft = true;
                     }
                     else
                     {
                         return false;
                     }
                 }
                 else if (dir == 1)
                 {
                     if (!cellGrid[x, y].traversedCircleRight)
                     {
                         cellGrid[x, y].traversedCircleRight = true;
                     }
                     else
                     {
                         return false;
                     }
                 }
                 else
                 {
                     return true;
                 }

                 return false;
             }
             /**/
             return true;
         }
        public void CellGridToBlockGrid()
        {
            grid = new BlockType[xGridLen,yGridLen];
            for (int x = 0; x < xGridLen; x++)
            {
                for (int y = 0; y < yGridLen; y++)
                {
                    if (cellGrid[x, y].Platform != PlatformType.NotPlatform)
                    {
                        grid[x, y] = BlockType.Platform;
                        continue;
                    }
                    if (cellGrid[x, y].reachesCircle)
                    {
                        grid[x, y] = BlockType.CircleCanReach;
                        if (cellGrid[x, y].reachesRectangle)
                        {
                            grid[x, y] = BlockType.BothCanReach;
                        }
                        continue;
                    }
                    if (cellGrid[x, y].reachesRectangle)
                    {
                        grid[x, y] = BlockType.RectangleCanReach;
                        continue;
                    }
                    /** /
                    if (cellGrid[x, y].fitsCircle)
                     {
                         grid[x, y] = BlockType.BothCanReach;
                         continue;
                     }
                     if (cellGrid[x, y].fitsRectangle)
                     {
                         grid[x, y] = BlockType.BothCanReach;
                         continue;
                     }
                     /**/
                    grid[x, y] = BlockType.Unreachable;
                }
            }
        }
    }
}