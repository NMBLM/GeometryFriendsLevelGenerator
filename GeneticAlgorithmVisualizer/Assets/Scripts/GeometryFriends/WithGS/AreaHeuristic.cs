using GeneticSharp.Domain.Fitnesses;
using System;
using System.Collections.Generic;
using System.Drawing;
using GeneticSharp.Domain.Chromosomes;
using GeneticSharp.Domain.Fitnesses;
using GeometryFriends.LevelGenerator;
using GeometryFriends.WithGS;
using UnityEngine;


namespace GeometryFriends.WithGS
{
    public class AreaHeuristic : IFitness
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
            public bool reachesCoop = false;
            public int jumpStrength = -1;
            //public bool cooperativeExclusive;
        }
        public float blockSize;
        public Cell[,] cellGrid;
        public BlockType[,] grid;
        public int xGridLen, yGridLen;
        public int rectangleMaxLen;
        public LevelSpecifications specs;
        
        
        public AreaHeuristic(LevelSpecifications spec, float blockSize = 16f)
        {
            
            this.blockSize = 16f;
            xGridLen = (int) ((1240 - 40) / this.blockSize + 0.5f) + 4; 
            yGridLen = (int) ((760 - 40) / this.blockSize + 0.5f) + 4; 

            rectangleMaxLen = (int) (200 / this.blockSize + 0.5f);

            cellGrid = new Cell[xGridLen,yGridLen];

            specs = spec;
        }
        
        public double CalculateFitness(LevelDNA level)
        {
            /** /
            if (!(level.collectibles.Count > 0))
            {
                InitGrid(level);
                return 0;
            }
            /**/
            InitGrid(level);
            InitFits();
            RectangleReachability(level);
            CircleReachability(level);
            ResetJumpStrength();
            CoopReachability(level);
            CellGridToBlockGrid();
            var fit =  fitness(level,specs);
            return fit;
        }

        private double fitness(LevelDNA level, LevelSpecifications spec)
        {
            if (!(spec.areas.Count > 0))
            {
                Debug.Log("No Specified Areas");
                return 1;
            }
            
            double fullAreaPercent = 0;
            double minArea = 2;
            foreach (var area in spec.areas)
            {
                double AreaPercent = 0;
                int areaPosX = (int) ((area.position.X - 40) / this.blockSize) + 2;
                int areaPosY = (int) ((area.position.Y - 40) / this.blockSize) + 2;
                int areaWidth = (int) (area.width / this.blockSize + 0.5f);
                int areaHeight = (int) (area.height / this.blockSize + 0.5f);
                
                AreaType type = area.type;

                for (int i = areaPosX; i < (areaPosX + areaWidth) && i < xGridLen; i++)
                {
                    for (int j = areaPosY; j < (areaPosY + areaHeight) && j < yGridLen; j++)
                    {
                        if (i > xGridLen || j > yGridLen || i < 0 || j < 0)
                        {
                            continue;
                        }
                        switch (type)
                        {
                            case AreaType.Common:
                                switch (grid[i,j])
                                {
                                    case BlockType.BothCanReach:
                                        AreaPercent += 1;
                                        break;
                                }
                                break;
                            case AreaType.Cooperative:
                                switch (grid[i,j])
                                {
                                    case BlockType.CooperativeCanReach:
                                        AreaPercent += 1;
                                        break;
                                    case BlockType.CooperativeCanReachRectanglePlatform:
                                        AreaPercent += 1;
                                        break;
                                }
                                break;
                            case AreaType.CircleOnly:
                                switch (grid[i,j])
                                {
                                    case BlockType.CircleCanReach:
                                        AreaPercent += 1;
                                        break;
                                    case BlockType.CircleCanReachRectanglePlatform:
                                        AreaPercent += 1;
                                        break;
                                }
                                break;
                            case AreaType.RectangleOnly:
                                switch (grid[i,j])
                                {
                                    case BlockType.RectangleCanReach:
                                        AreaPercent += 1;
                                        break;
                                    case BlockType.RectangleCanReachCirclePlatform:
                                        AreaPercent += 1;
                                        break;
                                }
                                break;
                        }
                    }
                }

                AreaPercent = AreaPercent / (areaWidth * areaHeight);
                fullAreaPercent += AreaPercent;
                minArea = Math.Min(AreaPercent, minArea);
            }
            if (minArea > 0) return minArea;
            return 0.0000000001;
            //return fullAreaPercent / spec.areas.Count;
            //return minArea * 0.8 + fullAreaPercent * 0.2;
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
                        cellGrid[i, j].Platform = plat.platformType;
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
                                stillFitCircle = false;
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

        public void ResetJumpStrength()
        {
            for (int i = 0; i < xGridLen; i++)
            {
                for (int j = 0; j < yGridLen; j++)
                {

                    cellGrid[i, j].jumpStrength = -1;


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
                            for (int i = 0; i < 3; i++)
                            {
                                list.Add(new Tuple<Point,int>(new Point(x-1, y-i),-1));
                            }   
                        }

                        if (cellGrid[x + 1, y].jumpStrength < 24)
                        {
                            list.Add(new Tuple<Point, int>(new Point(x + 1, y), 1));
                            for (int i = 0; i < 3; i++)
                            {
                                list.Add(new Tuple<Point,int>(new Point(x+1, y-i),1));
                            }   
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
                                    list.Add(new Tuple<Point, int>(new Point(x + j, y - 1), j));
                                }
                            }

                            if ((cellGrid[x, y].jumpStrength - 1 == 0 || !cellGrid[x, y-1].fitsCircle) 
                                && (cellGrid[x + dir, y].jumpStrength < 1))
                            {
                                list.Add(new Tuple<Point, int>(new Point(x + dir, y), dir));
                            }
                        }
                        else // free fall
                        /**/
                        {
                            freefalling += 1;
                            list.Add(new Tuple<Point,int>(new Point(x, y+1),0));
                            /**/
                            if (dir != 0)
                            {
                                if (cellGrid[x + dir, y + 1].fitsCircle)
                                {
                                    list.Add(new Tuple<Point, int>(new Point(x + dir, y + 1), dir));
                                }
                                else
                                {
                                    list.Add(new Tuple<Point, int>(new Point(x - dir, y + 1), -dir));
                                }
                            }
                        }
                       
                    }
                    /**/
                }

            }
            //Debug.Log(list.Count +" ; "+ cellsChecked + " : "+ freefalling);
        }
        
        public void CoopReachability(LevelDNA level)
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

                if (cellGrid[x, y].jumpStrength == 30)
                {
                    continue;
                }
                /**/
                if (cellGrid[x, y].fitsCircle)
                {
                    if (!cellGrid[x, y].reachesCircle)
                    {
                        cellGrid[x, y].reachesCoop = true;
                    }
                    //Check On the Ground
                    if (!cellGrid[x, y + 1].fitsCircle)
                    {
                        if (cellGrid[x, y].reachesRectangle)
                        {
                            cellGrid[x, y].jumpStrength = 30;

                            if (cellGrid[x - 1, y].jumpStrength < 30)
                            {
                                list.Add(new Tuple<Point, int>(new Point(x - 1, y), -1));
                            }

                            if (cellGrid[x + 1, y].jumpStrength < 30)
                            {
                                list.Add(new Tuple<Point, int>(new Point(x + 1, y), 1));
                            }

                            for (int i = -1; i < 1; i++)
                            {
                                if (cellGrid[x + i, y - 1].jumpStrength < 29)
                                {
                                    cellGrid[x + i, y - 1].jumpStrength = 29;
                                    list.Add(new Tuple<Point, int>(new Point(x + i, y - 1), i));
                                }
                            }  
                        }
                        else
                        {
                            //if(!(cellGrid[x, y].jumpStrength >= 24)) continue;
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
                    }
                    /**/
                    /**/
                    else // Mid-air
                    {
                        /**/
                        //if mid jump
                        if (cellGrid[x, y].jumpStrength > 0 && cellGrid[x, y].jumpStrength < 30)
                        {
                            for (int j = -1; j <= 1; j++)
                            {
                                
                                if (cellGrid[x + j, y - 1].jumpStrength < cellGrid[x, y].jumpStrength - 1)
                                {
                                    cellGrid[x + j, y - 1].jumpStrength = cellGrid[x, y].jumpStrength - 1;
                                    list.Add(new Tuple<Point, int>(new Point(x + j, y - 1), j));
                                }
                            }

                            if ((cellGrid[x, y].jumpStrength - 1 == 0 || !cellGrid[x, y-1].fitsCircle) 
                                && (cellGrid[x + dir, y].jumpStrength < 1))
                            {
                                list.Add(new Tuple<Point, int>(new Point(x + dir, y), dir));
                            }
                        }
                        else // free fall
                        /**/
                        {
                            freefalling += 1;
                            list.Add(new Tuple<Point,int>(new Point(x, y+1),0));
                            /**/
                            if (dir != 0)
                            {
                                if (cellGrid[x + dir, y + 1].fitsCircle)
                                {
                                    list.Add(new Tuple<Point, int>(new Point(x + dir, y + 1), dir));
                                }
                                else
                                {
                                    list.Add(new Tuple<Point, int>(new Point(x - dir, y + 1), -dir));
                                }
                            }
                        }
                       
                    }
                    /**/
                }

            }
            //Debug.Log(list.Count +" ; "+ cellsChecked + " : "+ freefalling);
        }

        public void CellGridToBlockGrid()
        {
            grid = new BlockType[xGridLen,yGridLen];
            for (int x = 0; x < xGridLen; x++)
            {
                for (int y = 0; y < yGridLen; y++)
                {
                    if (cellGrid[x, y].Platform == PlatformType.Common)
                    {
                        grid[x, y] = BlockType.Platform;
                        continue;
                    }
                    
                    if (cellGrid[x, y].Platform != PlatformType.NotPlatform)
                    {
                        grid[x, y] = BlockType.Platform;
                        continue;
                    }

                    if (cellGrid[x, y].reachesCoop)
                    {
                        grid[x, y] = BlockType.CooperativeCanReach;
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
                        if (cellGrid[x, y].reachesCircle)
                        {
                            grid[x, y] = BlockType.BothCanReach;
                        }
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

        public double Evaluate(IChromosome chromosome)
        {
            LevelDNA level;
            
            if (chromosome.GetType() == typeof(LevelChromosome))
            {
                var c = (LevelChromosome) chromosome;
                level = c.GetLevelDNA();

            }
            else if (chromosome.GetType() == typeof(SmallerLevelChromosome))
            {
                var c = (SmallerLevelChromosome) chromosome;
                level = c.GetLevelDNA();

            }
            else
            {
                return 0;
            }
            
            var fit = CalculateFitness(level);
            //chromosome.Fitness = fit;
            return fit;
        }

        public override string ToString()
        {
            var s = "Area Heurisitc\n";

            s += specs;

            return s;
        }
    }
}